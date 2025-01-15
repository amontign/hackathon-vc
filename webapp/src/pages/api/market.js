import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY, // Enter your OPENAI_API key
});

export default async (req, res) => {
    if (req.method !== 'GET') {
        console.log("HTTP Method not allowed:", req.method);
        return res.status(405).json({ message: 'Method not allowed' });
    }

    const { text } = req.query;

    if (!text) {
        console.log("Error: No text provided!");
        return res.status(400).json({ message: "Missing text" });
      }
    try {
        console.log("Received text:", text);
        console.log("Sending request to OpenAI API...");
        // Send a request to the OpenAI API
        const response = await openai.chat.completions.create({
          model: "gpt-4o-mini", // Model to use
          messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: `Provide a comprehensive analysis of the ${text} market for venture capital purposes. Structure your response as a JSON object with the following keys:

{
  "market_analysis": {
    "current_state": {"description": "", "key_trends": [], "sources": []},
    "growth_projection": {"forecast": "", "timeframe": "", "sources": []},
    "innovation_areas": {"description": "", "examples": [], "sources": []},
    "future_prospects": {"description": "", "potential_shifts": [], "sources": []},
    "challenges": {"description": "", "major_obstacles": [], "sources": []},
    "ai_use_cases": {"description": "", "examples": [], "sources": []},
    "key_players": {"established": [], "startups": [], "sources": []},
    "regulatory_landscape": {"description": "", "potential_changes": [], "sources": []},
    "investment_analysis": {"opportunities": [], "risks": [], "sources": []},
    "global_dynamics": {"description": "", "regional_variations": [], "sources": []},
    "customer_behavior": {"shifts": [], "evolving_needs": [], "sources": []},
    "competitive_landscape": {"description": "", "key_competitors": [], "sources": []},
    "exit_strategies": {"description": "", "potential_strategies": [], "sources": []},
    "top_performer_analysis": {"productivity_metrics": {}, "specialization_strategies": "", "quality_impact": "", "organizational_culture": "", "value_creation": "", "sources": []},
    "talent_landscape": {"skill_scarcity": "", "retention_challenges": [], "top_talent_impact": "", "data_driven_approaches": [], "sources": []},
    "high_performer_strategies": {"description": "", "examples": [], "sources": []}
  }
}

Include relevant data, statistics, and expert opinions where applicable, always citing the sources. For any conflicting information, include it in the respective section with a note on the discrepancy and its sources. Provide insights on how these factors might influence investment decisions and long-term market positioning, referencing successful VC strategies or market entry case studies where possible.` },
          ],
        });
        console.log("OpenAI API Response:", response.choices[0].message.content);
        res.status(200).json({
            user_input: text,
            reply: response.choices[0].message.content,
        });
    } 
    catch (error) {
        // Log error details if the request fails
        console.error("Error calling OpenAI API:", error.response?.data || error.message);
        res.status(500).json({ message: "An error occurred while processing your request."});
    }
}
