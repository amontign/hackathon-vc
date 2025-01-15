

export default async (req, res) => {
    if (req.method !== 'GET') {
        return res.status(405).json({ message: 'Method not allowed' });
    }

    const { text } = req.query;

    if (!text) {
        return res.status(400).json({ message: 'Missing text' });
    }
    res.status(200).json({ market: text });
}