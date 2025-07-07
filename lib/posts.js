import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import { remark } from 'remark'
import html from 'remark-html'

const postsDir = path.join(process.cwd(), 'posts')

export function getPostSlugs() {
  return fs.readdirSync(postsDir)
}

export async function getPostBySlug(slug) {
  const realSlug = slug.replace(/\.md$/, '')
  const fullPath = path.join(postsDir, `${realSlug}.md`)
  const fileContents = fs.readFileSync(fullPath, 'utf8')
  const { data, content } = matter(fileContents)
  const processedContent = await remark().use(html).process(content)
  return {
    slug: realSlug,
    meta: data,
    content: processedContent.toString(),
  }
}

export async function getAllPosts() {
  const slugs = getPostSlugs()
  const posts = await Promise.all(
    slugs.map(async (slug) => await getPostBySlug(slug))
  )
  // Puedes ordenar por fecha si incluyes un campo `date` en frontmatter
  return posts
}
