import Link from 'next/link'
export default function Header() {
  return (
    <header className="p-4 bg-gray-100 flex justify-between items-center">
      <div className="text-xl font-bold">Cafeteras Portátiles</div>
      <nav>
        <Link href="/">Inicio</Link> | 
        <Link href="/about">Sobre nosotros</Link> | 
        <Link href="/faq">FAQ</Link> | 
        <Link href="/contact">Contacto</Link>
      </nav>
    </header>
  )
}
