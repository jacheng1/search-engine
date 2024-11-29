'use client'

import { useState } from "react";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query) {
      return;
    }
    setLoading(true);

    try {
      const response = await fetch(`/api/search?query=${encodeURIComponent(query)}`);
      const data = await response.json();

      if (response.ok) {
        setResults(data.results);
      } else {
        console.error("Error:", data.error);
      }
    } catch (error) {
      console.error("Error fetching results:", error);

    } finally {
      setLoading(false);

    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Search Engine</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query"
        style={{
          padding: "10px",
          width: "300px",
          marginRight: "10px",
          fontSize: "16px",
        }}
      />
      <button onClick={handleSearch} style={{ padding: "10px 20px", fontSize: "16px" }}>
        Search
      </button>
      {loading && <p>Loading...</p>}
      <ul>
        {results.map((result, index) => (
          <li key={index}>
            <a href={result[0]} target="_blank" rel="noopener noreferrer">
              {result[0]} (Score: {result[1].toFixed(2)})
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}