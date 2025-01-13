import dotenv from "dotenv";
dotenv.config();
import puppeteer from "puppeteer";
import OpenAI from "openai";
import fs from "fs/promises";

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

async function fetchContentFromJson(filePath) {
    try {
        console.log(`Reading content from JSON file: ${filePath}`);
        const data = await fs.readFile(filePath, "utf8");
        const json = JSON.parse(data);

        // Extract relevant content for analysis
        return json.map(item => ({
            title: item.title || "",
            comments: item.comments || [],
        }));
    } catch (error) {
        console.error("Error reading JSON file:", error.message);
        return null;
    }
}

async function analyzeSentiment(content) {
    try {
        console.log("Analyzing sentiment...");
        const response = await openai.chat.completions.create({
            model: "gpt-4o",
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
        console.log("Sentiment Score:", numericScore);
        return numericScore;
    } catch (error) {
        console.error("Error analyzing sentiment:", error.message);
        console.error("Skipping this entry due to error.");
        return null;
    }
}

async function processInput(input, type) {
    let content;

    if (type === "url") {
        content = await fetchContentFromUrl(input);
    } else if (type === "json") {
        content = await fetchContentFromJson(input);
    } else {
        console.error("Invalid input type. Use 'url' or 'json'.");
        return null;
    }

    if (!content) {
        console.error(`No content found for input type: ${type}, input: ${input}`);
        return null;
    }

    let allSentiments = [];

    if (type === "json") {
        for (const item of content) {
            const { title, comments } = item;

            // Analyze title
            const titleSentiment = await analyzeSentiment(title);
            if (titleSentiment !== null) allSentiments.push(titleSentiment);

            // Analyze comments
            for (const comment of comments) {
                const commentSentiment = await analyzeSentiment(comment);
                if (commentSentiment !== null) allSentiments.push(commentSentiment);
            }
        }
    } else {
        // For URL content
        const summary = await summarizeContent(content);
        const sentimentScore = await analyzeSentiment(summary);
        if (sentimentScore !== null) allSentiments.push(sentimentScore);
    }

    return allSentiments;
}

async function processAllSources(inputs) {
    let allSentiments = [];

    for (const { input, type } of inputs) {
        console.log(`Processing input from ${type}...`);
        const sentiments = await processInput(input, type);
        if (sentiments) allSentiments = allSentiments.concat(sentiments);
    }

    // Calculate average sentiment
    const totalSentiments = allSentiments.length;
    const averageSentiment =
        totalSentiments > 0
            ? allSentiments.reduce((sum, score) => sum + score, 0) / totalSentiments
            : 0;

    const result = { averageSentiment: parseFloat(averageSentiment.toFixed(2)) };

    // Save result to a JSON file
    const outputFilePath = "average_sentiment_result.json";
    await fs.writeFile(outputFilePath, JSON.stringify(result, null, 2), "utf8");
    console.log(`\nAverage Sentiment Score has been saved to ${outputFilePath}`);
}

(async () => {
    const inputs = [
        { input: "youtube_comments.json", type: "json" },
        { input: "articles.json", type: "json" },
    ];

    await processAllSources(inputs);
})();
