const express = require("express");
const cors = require("cors");

const app = express();   

app.use(cors());        
app.use(express.json());

// Sample route
app.get("/logs", (req, res) => {
  res.json([
    { ip: "192.168.1.10", attack: "Brute Force", severity: "High" },
    { ip: "10.0.0.5", attack: "SQL Injection", severity: "Critical" }
  ]);
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
