'use client'

import SearchIcon from "@mui/icons-material/Search";
import { Box, TextField, Typography, InputAdornment, IconButton } from "@mui/material";
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

  const colors = ["#4285F4", "#EA4335", "#FBBC05", "#34A853"];
  const text = "Zotsearch";

  return (
    <>
      <Box style={{ padding: "25px", fontFamily: "Arial, sans-serif" }}>
        <Box
          style={{
            display: "flex",
            alignItems: "center",
            gap: "40px",
            marginBottom: "20px"
          }}
        >
          <Typography variant="h4" component="div" style={{ display: "flex", alignItems: "center", margin: 0 }}>
            {text.split("").map((char, index) => (
              <span
                key={index}
                style={{
                  color: colors[index % colors.length]
                }}
              >
                {char}
              </span>
            ))}
          </Typography>
          <Box style={{ display: "flex", alignItems: "center" }}>
            <TextField
              variant="outlined"
              placeholder="Search Zotsearch"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if ((e.key === "Enter") && (e !== "")) {
                  handleSearch();
                }
              }}
              InputProps={{
                style: { borderRadius: "25px" },
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={handleSearch}>
                      <SearchIcon sx={{ color: "#4285F4" }}/>
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              style={{ width: "750px" }}
            />
          </Box>
        </Box>
      </Box>
      <div
        style={{
          borderTop: "1px solid lightgray",
          width: "100%",
          marginLeft: 0,
          marginRight: 0,
          marginBottom: "20px"
        }}
      ></div>
      <Box style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
        {loading && <Typography variant="h6">Loading...</Typography>}
        {results.map((result, index) => (
          <Typography key={index}>
            <a href={result[0]} target="_blank" rel="noopener noreferrer">
              {result[0]} (Score: {result[1].toFixed(2)})
            </a>
          </Typography>
        ))}
      </Box>
    </>
  );
}