export default function Home() {
  return (
    <main>
      <iframe
        className="research-site"
        src="/explorer/index.html"
        title="Precision radial-velocity spectrograph landscape"
      />
      <noscript>
        <p>
          JavaScript is required for the filterable evidence table. The source
          tables and report remain available in the GitHub repository.
        </p>
      </noscript>
    </main>
  );
}
