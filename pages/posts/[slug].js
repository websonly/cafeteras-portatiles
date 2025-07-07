jsx
// pages/posts/[slug].js

import Head from 'next/head'
import { getPostSlugs, getPostBySlug } from '../../lib/posts'
import styles from '../../styles/post.module.css'

export default function PostPage({ post }) {
  return (
    <>
      <Head>
        <title>{post.meta.title} | Cafeteras Portátiles</title>
        <meta name="description" content={post.excerpt || post.meta.title} />
      </Head>

      <article className={styles.container}>
        <h1 className={styles.title}>{post.meta.title}</h1>
        <time className={styles.date} dateTime={post.meta.date}>
          {new Date(post.meta.date).toLocaleDateString()}
        </time>
        <div
          className={styles.content}
          dangerouslySetInnerHTML={{ __html: post.contentHtml }}
        />
      </article>
    </>
  )
}

export async function getStaticPaths() {
  const slugs = getPostSlugs()
  const paths = slugs.map((slug) => ({ params: { slug } }))
  return { paths, fallback: false }
}

export async function getStaticProps({ params }) {
  const post = getPostBySlug(params.slug)
  return {
    props: { post }
  }
}

