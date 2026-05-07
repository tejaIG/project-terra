export default function DocsPage() {
  return (
    <main
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        fontFamily: "system-ui, sans-serif",
        gap: "1rem",
      }}
    >
      <h1 style={{ fontSize: "2.5rem", fontWeight: 700 }}>📚 Docs App</h1>
      <p style={{ color: "#555", fontSize: "1.1rem" }}>
        Documentation site for <strong>Project Terra</strong> Turborepo monorepo.
      </p>
      <p style={{ color: "#999", fontSize: "0.9rem" }}>Running on port 3001</p>
    </main>
  );
}
