export default function Footer() {
  return (
    <footer className="p-4 bg-gray-200 text-center text-sm">
      © {new Date().getFullYear()} Cafeteras Portátiles. 
      <a href="/privacy">Política de privacidad</a> | 
      <a href="/legal">Aviso legal</a>
    </footer>
  )
}
