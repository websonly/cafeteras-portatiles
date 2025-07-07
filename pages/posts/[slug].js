import { getPostSlugs, getPostBySlug } from '../../lib/posts'

export async function getStaticPaths() {
  const slugs = getPostSlugs().map((s) => s.replace(/\.md$/, ''))
  return {
    paths: slugs.map((slug) => ({ params: { slug } })),
    fallback: false,
  }
}

export async function getStaticProps({ params }) {
  const post = await getPostBySlug(params.slug)
  return { props: { post } }
}

export default function PostPage({ post }) {
  const { meta, content } = post
  return (
    <>
      <h1 className="text-3xl font-bold mb-2">{meta.title}</h1>
      {meta.date && (
        <p className="text-sm text-gray-500 mb-4">{meta.date}</p>
      )}
      <div
        className="prose max-w-none"
        dangerouslySetInnerHTML={{ __html: content }}
      />
    </>
  )
}
