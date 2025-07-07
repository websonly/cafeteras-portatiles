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
  const title = meta.title
  const description = meta.description || meta.title
  const url = `https://cafeterasportatiles.online/posts/${post.slug}`
  const image = meta.image || '/default-og-image.jpg'
  return (
  <>
    <Head>
      <title>{title}</title>
      <meta name="description" content={description} />

      {/* Open Graph */}
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:type" content="article" />
      <meta property="og:url" content={url} />
      <meta property="og:image" content={image} />

      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={image} />
    </Head>
    {/* resto de tu contenido */}
    <h1 className="text-3xl font-bold mb-2">{meta.title}</h1>
    …
  </>
)

}
