export async function onRequest(context) {
  const slug = context.params.slug;
  return new Response(`Slug: ${slug}`);
}
