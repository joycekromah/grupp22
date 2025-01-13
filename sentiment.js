import dotenv from "dotenv";
dotenv.config();
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

async function analyzeSentiment(content) {
    try {
        const response = await openai.chat.completions.create({
            model: "gpt-3.5-turbo",
            messages: [
                { role: "system", content: "You are a sentiment analysis assistant." },
                {
                    role: "user",
                    content: `Analyze the sentiment of the following text, where -5 is very negative, 0 is neutral, and +5 is very positive. Provide only the numerical sentiment score:\n\n${content}`,
                },
            ],
        });
        const sentimentScore = response.choices[0].message.content.trim();
        const numericScore = parseFloat(sentimentScore);

        if (isNaN(numericScore)) {
            console.error(`Invalid sentiment score returned: "${sentimentScore}". Skipping this entry.`);
            return null;
        }
        return numericScore;
    } catch (error) {
        console.error("Error analyzing sentiment:", error.message);
        return null;
    }
}

async function processContent(data) {
    const allSentiments = [];

    for (const source in data) {
        const items = data[source];
        for (const item of items) {
            const titleSentiment = await analyzeSentiment(item.title);
            if (titleSentiment !== null) allSentiments.push(titleSentiment);


            if (item.comments) {
                for (const comment of item.comments) {
                    const commentSentiment = await analyzeSentiment(comment);
                    if (commentSentiment !== null) allSentiments.push(commentSentiment);
                }
            }
        }
    }

    const averageSentiment = allSentiments.length
        ? allSentiments.reduce((sum, score) => sum + score, 0) / allSentiments.length
        : 0;

    return { averageSentiment: parseFloat(averageSentiment.toFixed(2)) };
}

(async () => {
    const inputData = await new Promise((resolve) => {
        let input = "";
        process.stdin.on("data", (chunk) => (input += chunk));
        process.stdin.on("end", () => resolve(JSON.parse(input)));
    });

    const result = await processContent(inputData);
    console.log(JSON.stringify(result));
})();