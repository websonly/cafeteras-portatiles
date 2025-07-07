export default function Contact() {
  return (
    <>
      <h1 className="text-2xl font-bold mb-4">Contacto</h1>
      <form
        name="contact"
        method="POST"
        data-netlify="true"
        className="flex flex-col gap-4 max-w-md"
      >
        <input type="hidden" name="form-name" value="contact" />
        <label>
          Nombre:
          <input type="text" name="name" required className="border p-2 w-full" />
        </label>
        <label>
          Email:
          <input type="email" name="email" required className="border p-2 w-full" />
        </label>
        <label>
          Mensaje:
          <textarea name="message" required className="border p-2 w-full" />
        </label>
        <button
          type="submit"
          className="bg-blue-600 text-white py-2 px-4 rounded"
        >
          Enviar
        </button>
      </form>
    </>
  )
}
