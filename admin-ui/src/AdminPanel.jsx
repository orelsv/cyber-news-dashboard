import React, { useEffect, useState } from "react";

export default function AdminPanel() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState("");
  const [form, setForm] = useState({
    keywords: "cybersecurity, malware, phishing",
    article_count: 12,
    refresh_minutes: 30
  });

  useEffect(() => {
    // Load current settings from Flask
    fetch("/api/settings")
      .then((r) => r.json())
      .then((data) => {
        setForm({
          keywords: data.keywords ?? "",
          article_count: data.article_count ?? 10,
          refresh_minutes: data.refresh_minutes ?? 30
        });
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const onChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: name === "article_count" || name === "refresh_minutes" ? Number(value) : value }));
  };

  const onSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMsg("");
    try {
      const res = await fetch("/api/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error("Save failed");
      setMsg("Settings saved.");
    } catch (err) {
      setMsg("Error saving settings.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div style={wrapStyle}><div style={cardStyle}>Loading...</div></div>;

  return (
    <div style={wrapStyle}>
      <div style={cardStyle}>
        <h1 style={{ margin: 0, fontSize: 28 }}>Admin Panel</h1>
        <p style={{ opacity: 0.7, marginTop: 6 }}>Customize it for yourself</p>

        <form onSubmit={onSave} style={{ marginTop: 20, display: "grid", gap: 16 }}>
          <div>
            <label style={labelStyle}>Keywords (comma separated)</label>
            <input
              name="keywords"
              value={form.keywords}
              onChange={onChange}
              style={inputStyle}
              placeholder="e.g. cybersecurity, malware, phishing"
            />
          </div>

          <div>
            <label style={labelStyle}>Articles to show</label>
            <input
              type="number"
              min="1"
              max="50"
              name="article_count"
              value={form.article_count}
              onChange={onChange}
              style={inputStyle}
            />
          </div>

          <div>
            <label style={labelStyle}>Refresh interval (minutes)</label>
            <input
              type="number"
              min="1"
              max="180"
              name="refresh_minutes"
              value={form.refresh_minutes}
              onChange={onChange}
              style={inputStyle}
            />
          </div>

          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <button type="submit" disabled={saving} style={btnStyle}>
              {saving ? "Saving..." : "Save settings"}
            </button>
            {msg && <span>{msg}</span>}
          </div>
        </form>

        <div style={{ marginTop: 24, paddingTop: 16, borderTop: "1px solid #e5e5e5" }}>
          <p style={{ margin: 0, opacity: 0.7 }}>
            Open site: <a href="/" style={{ color: "#0071e3", textDecoration: "none" }}>News Feed</a>
          </p>
        </div>
      </div>
    </div>
  );
}

const wrapStyle = {
  minHeight: "100svh",
  background: "linear-gradient(180deg, #fafafa, #f3f3f3)",
  display: "grid",
  placeItems: "center",
  padding: "32px",
};

const cardStyle = {
  width: "100%",
  maxWidth: 720,
  margin: "0 auto",        // center horizontally
  background: "#ffffff",
  borderRadius: 24,
  boxShadow: "0 8px 36px rgba(0,0,0,0.08)",
  padding: 24,             // uniform padding is enough
  border: "1px solid #eee",
  boxSizing: "border-box", // ensures padding is included in width
};

const labelStyle = {
  display: "block",
  fontSize: 14,
  marginBottom: 8,
  fontWeight: 600,
};

const inputStyle = {
  width: "100%",             // fill container width
  boxSizing: "border-box",   // ✅ include padding in width
  height: 44,
  borderRadius: 12,
  border: "1px solid #ddd",
  padding: "0 12px",
  outline: "none",
  fontSize: 16,
  background: "#fff",
};

const btnStyle = {
  height: 44,
  padding: "0 18px",
  borderRadius: 12,
  border: "none",
  fontWeight: 700,
  background: "#000",
  color: "#fff",
  cursor: "pointer",
};

