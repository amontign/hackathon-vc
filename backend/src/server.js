const express = require("express");
const Database = require("better-sqlite3");
const { v4: uuidv4 } = require("uuid");
const swaggerUi = require("swagger-ui-express");
const YAML = require("yamljs");
const path = require("path");

const app = express();
const port = process.env.PORT || 3000;

// Initialize SQLite database
const db = new Database("research.db");

// Create table if it doesn't exist
db.exec(`
  CREATE TABLE IF NOT EXISTS research_flows (
    uuid TEXT PRIMARY KEY,
    status TEXT CHECK(status IN ('Collecting', 'Summarizing', 'Done')) NOT NULL,
    result TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

// Load Swagger document
const swaggerDocument = YAML.load(path.join(__dirname, "swagger.yaml"));
app.use("/api", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Middleware to validate UUID
const validateUUID = (req, res, next) => {
  const uuid = req.query.uuid;
  if (!uuid) {
    return res.status(400).json({ error: "UUID parameter is required" });
  }

  const uuidRegex =
    /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  if (!uuidRegex.test(uuid)) {
    return res.status(400).json({ error: "Invalid UUID format" });
  }

  next();
};

// Create new research flow
app.get("/create", (req, res) => {
  const term = req.query.term;
  if (!term) {
    return res.status(400).json({ error: "Term parameter is required" });
  }

  const uuid = uuidv4();

  try {
    const stmt = db.prepare(
      "INSERT INTO research_flows (uuid, status) VALUES (?, ?)"
    );
    stmt.run(uuid, "Collecting");

    // Here trigger research flow process
    // For now, we just return the UUID

    res.json({ uuid });
  } catch (error) {
    console.error("Database error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Get status of research flow
app.get("/status", validateUUID, (req, res) => {
  try {
    const stmt = db.prepare("SELECT status FROM research_flows WHERE uuid = ?");
    const result = stmt.get(req.query.uuid);

    if (!result) {
      return res.status(404).json({ error: "Research flow not found" });
    }

    res.json({ status: result.status });
  } catch (error) {
    console.error("Database error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Get result of research flow
app.get("/result", validateUUID, (req, res) => {
  try {
    const stmt = db.prepare(
      "SELECT status, result FROM research_flows WHERE uuid = ?"
    );
    const result = stmt.get(req.query.uuid);

    if (!result) {
      return res.status(404).json({ error: "Research flow not found" });
    }

    if (result.status !== "Done") {
      return res.status(400).json({
        error: "Research is not complete yet",
        status: result.status,
      });
    }

    res.json({ result: result.result });
  } catch (error) {
    console.error("Database error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
  console.log(
    `API documentation available at http://localhost:${port}/api`
  );
});
