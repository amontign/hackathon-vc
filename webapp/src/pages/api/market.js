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
            { role: "user", content: text },
          ],
        });
        console.log("OpenAI API Response:", response.data);
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
