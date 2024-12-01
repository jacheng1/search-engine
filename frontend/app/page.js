'use client'

import ClearIcon from "@mui/icons-material/Clear";
import SearchIcon from "@mui/icons-material/Search";
import { Box, TextField, Typography, InputAdornment, IconButton } from "@mui/material";
import { useState } from "react";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [responseTime, setResponseTime] = useState(null);
  const [searchPerformed, setSearchPerformed] = useState(false);

  const handleSearch = async () => {
    if (!query) {
      return;
    }

    setLoading(true);
    setSearchPerformed(true);

    try {
      const response = await fetch(`/api/search?query=${encodeURIComponent(query)}`);
      const data = await response.json();

      if (response.ok) {
        setResults(data.results);
        setResponseTime(data.response_time);

      } else {
        console.error("Error:", data.error);

      }
    } catch (error) {
      console.error("Error fetching results:", error);

    } finally {
      setLoading(false);

    }
  };

  const handleClear = () => {
    setQuery("");
  };

  const colors = ["#4285F4", "#EA4335", "#FBBC05", "#34A853"];
  const text = "Zotsearch";

  const formatTitle = (text, threshold) => {
    if (!text) {
      return "No Title Available";
    }

    let formattedText = "";
    let words = text.split(" ");
    let currentLength = 0;
  
    for (let word of words) {
      if (currentLength + word.length > threshold) {
        formattedText += "\n";

        currentLength = 0;
      }

      formattedText += word + " ";

      currentLength += word.length + 1;
    }
  
    return formattedText.trim();
  };

  const formatDescription = (description, threshold) => {
    if (!description) {
      return "No Description Available";
    }

    let formattedDescription = "";
    let words = description.split(" ");
    let currentLength = 0;
  
    for (let word of words) {
      if (currentLength + word.length > threshold) {
        formattedDescription += "\n";

        currentLength = 0;
      }

      formattedDescription += word + " ";

      currentLength += word.length + 1;
    }
  
    return formattedDescription.trim();
  };

  return (
    <>
      <Box style={{ padding: "25px", fontFamily: "Arial, sans-serif" }} sx={{ backgroundColor: "#F8F9FA" }}>
        <Box
          style={{
            display: "flex",
            alignItems: "center",
            gap: "40px",
            marginBottom: "10px"
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
                style: { borderRadius: "25px", backgroundColor: "#FFFFFF" },
                endAdornment: (
                  <InputAdornment position="end">
                    {query && (
                      <IconButton onClick={handleClear}>
                        <ClearIcon sx={{ color: "#5F6368" }} />
                      </IconButton>
                    )}
                    {query && (
                      <Box
                        sx={{
                          width: "1px",
                          height: "36px",
                          backgroundColor: "lightgray",
                          margin: "0 8px"
                        }}
                      />
                    )}
                    <IconButton onClick={handleSearch}>
                      <SearchIcon sx={{ color: "#4285F4" }} />
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
          marginBottom: "10px"
        }}
      ></div>
      <Box style={{ padding: "20px", marginLeft: "210px", fontFamily: "Arial, sans-serif" }}>
        {searchPerformed && (
          <Typography
            style={{ fontFamily: "Arial, sans-serif" }}
            sx={{
              color: "#5F6368",
              fontSize: "15px",
              marginTop: "-20px",
              marginBottom: "20px",
            }}
          >
            About {results.length} results ({responseTime ? `${responseTime} seconds` : "N/A"})
          </Typography>
        )}
        {loading && <Typography variant="h6">Loading...</Typography>}
        {results.map((result, index) => (
          <Box key={index} sx={{ marginBottom: "20px" }}>
            <Typography sx={{ fontSize: "12px" }}>
              {result.domain}
            </Typography>
            <Typography sx={{ color: "#5F6368", fontSize: "12px", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
              {result.url}
            </Typography>
            <Typography 
              variant="h5" 
              sx={{ 
                color: "#5F6368",
                whiteSpace: "pre-line",
                wordBreak: "break-word",
                overflow: "hidden",
                textOverflow: "ellipsis",
                display: "-webkit-box",
                WebkitBoxOrient: "vertical",
                WebkitLineClamp: 3
              }}
            >
              <a 
                href={result.url} 
                target="_blank" 
                rel="noopener noreferrer" 
                style={{ textDecoration: "none" }}
              >
                {formatTitle(result.title, 70)}
              </a>
            </Typography>
            <Typography
              sx={{
                color: "#5F6368",
                whiteSpace: "pre-line",
                wordBreak: "break-word",
                overflow: "hidden",
                textOverflow: "ellipsis",
                display: "-webkit-box",
                WebkitBoxOrient: "vertical",
                WebkitLineClamp: 3
              }}
            >
              {formatDescription(result.description, 100)}
            </Typography>
          </Box>
        ))}
      </Box>
    </>
  );
}