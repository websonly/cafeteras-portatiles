// lib/posts.js

import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import { remark } from 'remark'
import html from 'remark-html'

const postsDir = path.join(process.cwd(), 'posts')

/**
 * Devuelve todos los slugs de las entradas,
 * sin la extensión “.md”
 */
export function getPostSlugs() {
  return fs
    .readdirSync(postsDir)
    .filter((file) => file.toLowerCase().endsWith('.md'))
    .map((file) => file.replace(/\.md$/i, ''))
}

/**
 * Lee un post a partir de su slug, procesa su frontmatter
 * y convierte el markdown a HTML serializable.
 */
export async function getPostBySlug(slug) {
  const realSlug = slug.replace(/\.md$/, '')
  const fullPath = path.join(postsDir, `${realSlug}.md`)
  const fileContents = fs.readFileSync(fullPath, 'utf8')
  const { data, content } = matter(fileContents)
  const processedContent = await remark().use(html).process(content)

  // Asegurar que la fecha devuelta sea un string ISO
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

/**
 * Recupera todos los posts y los ordena por fecha descendente
 */
export async function getAllPosts() {
  const slugs = getPostSlugs()
  const posts = await Promise.all(
    slugs.map(async (slug) => await getPostBySlug(slug))
  )
  return posts.sort((a, b) =>
    a.meta.date < b.meta.date ? 1 : a.meta.date > b.meta.date ? -1 : 0
  )
}
