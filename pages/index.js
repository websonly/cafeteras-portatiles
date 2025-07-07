export default function Home() {
  return (
    <main style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>¡Bienvenido a Cafeteras Portátiles!</h1>
      {/* BANNER TEMPORAL */}
      <div style={{
        margin: '2rem 0',
        padding: '1rem',
        border: '2px dashed #333',
        borderRadius: '8px',
        textAlign: 'center',
      }}>
        <h2>Promoción especial (temporal)</h2>
        <p>
          Haz clic abajo y adquiere este eBook de prueba por solo 0,99 €:
        </p>
        <a
          href="https://www.amazon.es/dp/B0CM6TM4T4/?tag=websonly-21"
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: 'inline-block',
            marginTop: '1rem',
            padding: '0.75rem 1.5rem',
            backgroundColor: '#ff9900',
            color: '#fff',
            textDecoration: 'none',
            borderRadius: '4px',
          }}
        >
          Comprar eBook de prueba
        </a>
      </div>
      {/* FIN BANNER TEMPORAL */}
      <p>Continúa explorando nuestras guías y comparativas…</p>
    </main>
  )
}
