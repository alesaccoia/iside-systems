export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6 py-12">
      <div className="max-w-md w-full space-y-12 text-center">
        <h1 className="text-3xl font-semibold tracking-tight text-foreground">
          Iside Systems SRLS
        </h1>

        <div className="space-y-6 text-muted-foreground text-sm">
          <div className="space-y-1">
            <p className="text-foreground">Via Tortona 12</p>
            <p>20144 Milano</p>
          </div>

          <div>
            <p>P.IVA 14733480967</p>
          </div>

          <div>
            <a
              href="tel:+393292038171"
              className="text-foreground hover:text-muted-foreground transition-colors"
            >
              +39 329 203 8171
            </a>
          </div>

          <div>
            <a
              href="mailto:iside.systems.srls@pec.it"
              className="text-foreground hover:text-muted-foreground transition-colors"
            >
              iside.systems.srls@pec.it
            </a>
          </div>

          <div>
            <a
              href="https://www.linkedin.com/in/alesaccoia/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-foreground hover:text-muted-foreground transition-colors"
            >
              LinkedIn
            </a>
          </div>

        </div>
      </div>
    </main>
  )
}
