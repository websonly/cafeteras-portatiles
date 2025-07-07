import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import { remark } from 'remark'
import html from 'remark-html'

const postsDir = path.join(process.cwd(), 'posts')

export function getPostSlugs() {
  return fs
    .readdirSync(postsDir)
    .filter((file) => file.toLowerCase().endsWith('.md'))
}

export async function getPostBySlug(slug) {
  const realSlug = slug.replace(/\.md$/, '')
  const fullPath = path.join(postsDir, `${realSlug}.md`)
  const fileContents = fs.readFileSync(fullPath, 'utf8')
  const { data, content } = matter(fileContents)
  const processedContent = await remark().use(html).process(content)

  // Asegurar que la fecha es serializable (string)
  let date = data.date
  if (date instanceof Date) {
    date = date.toISOString().split('T')[0]
  }

  return {
    slug: realSlug,
    meta: {
      ...data,
      date,
    },
    content: processedContent.toString(),
  }
}

export async function getAllPosts() {
  const slugs = getPostSlugs()
  const posts = await Promise.all(
    slugs.map(async (slug) => await getPostBySlug(slug))
  )
  // Opcional: ordenar por fecha descendente si meta.date existe
  return posts.sort((a, b) => (a.meta.date < b.meta.date ? 1 : -1))
}
