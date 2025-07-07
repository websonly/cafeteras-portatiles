import Link from 'next/link'
import { getAllPosts } from '../../lib/posts'

export async function getStaticProps() {
  const posts = await getAllPosts()
  return { props: { posts } }
}

export default function Posts({ posts }) {
  return (
    <>
      <h1 className="text-2xl font-bold mb-4">Últimos artículos</h1>
      <ul className="space-y-4">
        {posts.map(({ slug, meta }) => (
          <li key={slug}>
            <Link href={`/posts/${slug}`}>
              <a className="text-blue-600 hover:underline">{meta.title}</a>
            </Link>
            {meta.date && <span className="text-sm text-gray-500"> — {meta.date}</span>}
          </li>
        ))}
      </ul>
    </>
  )
}
