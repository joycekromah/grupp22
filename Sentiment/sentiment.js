import dotenv from "dotenv";
dotenv.config();
import puppeteer from "puppeteer";
import OpenAI from "openai";
import fs from "fs/promises";

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY, // Hämtas från .env
});

async function fetchContentFromUrl(url) {
    try {
        console.log(`Fetching content from: ${url}`);
        const browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();
        await page.goto(url, { waitUntil: "domcontentloaded" });
        const content = await page.evaluate(() => document.body.innerText);
        await browser.close();

        console.log("Fetched content (first 500 characters):", content.slice(0, 500));
        return content;
    } catch (error) {
        console.error("Error fetching URL:", error.message);
        return null;
    }
}

// Fetch content from a JSON file
async function fetchContentFromJson(filePath) {
    try {
        console.log(`Reading content from JSON file: ${filePath}`);
        const data = await fs.readFile(filePath, "utf8");
        const json = JSON.parse(data);
        return json.text || json.texts.join(" "); // Combine texts if it's an array
    } catch (error) {
        console.error("Error reading JSON file:", error.message);
        return null;
    }
}

// Summarize content
async function summarizeContent(content) {
    try {
        console.log("Summarizing content...");
        const response = await openai.chat.completions.create({
            model: "gpt-3.5-turbo",
            messages: [
                { role: "system", content: "You are a summarization assistant." },
                {
                    role: "user",
                    content: `Summarize the following content in a concise paragraph:\n\n${content}`,
                },
            ],
            max_tokens: 500,
        });
        const summary = response.choices[0].message.content.trim();
        console.log("Summary:", summary);
        return summary;
    } catch (error) {
        console.error("Error summarizing content:", error.message);
        return null;
    }
}

// Analyze sentiment of content
async function analyzeSentiment(content) {
    try {
        console.log("Analyzing sentiment...");
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
        console.log("Sentiment Score:", sentimentScore);
        return sentimentScore;
    } catch (error) {
        console.error("Error analyzing sentiment:", error.message);
        return null;
    }
}

// Process input from URL, JSON, or Text
async function processInput(input, type) {
    let content;

    if (type === "url") {
        content = await fetchContentFromUrl(input);
    } else if (type === "json") {
        content = await fetchContentFromJson(input);
    } else if (type === "text") {
        content = input;
    } else {
        console.error("Invalid input type. Use 'url', 'json', or 'text'.");
        return;
    }

    if (!content) {
        console.error(`No content found for input type: ${type}, input: ${input}`);
        return null;
    }

    const summary = await summarizeContent(content);
    if (!summary) {
        console.error("Failed to summarize content.");
        return null;
    }

    const sentimentScore = await analyzeSentiment(summary);
    if (sentimentScore !== null) {
        return { type, summary, sentimentScore };
    } else {
        console.error("Failed to analyze sentiment.");
        return null;
    }
}

// Main function to process all sources and compile results
async function processAllSources(inputs) {
    const results = [];

    for (const { input, type } of inputs) {
        console.log(`Processing input from ${type}...`);
        const result = await processInput(input, type);
        if (result) results.push(result);
    }

    console.log("\n--- Results ---");
    results.forEach((result, index) => {
        console.log(`Source ${index + 1} (${result.type}):`);
        console.log(`Summary: ${result.summary}`);
        console.log(`Sentiment Score: ${result.sentimentScore}`);
    });

    // Compile all sentiment scores into an average
    const scores = results.map((result) => parseFloat(result.sentimentScore));
    const averageScore = scores.reduce((sum, score) => sum + score, 0) / scores.length;
    console.log(`\nAverage Sentiment Score: ${averageScore.toFixed(2)}`);
}

(async () => {
    const inputs = [
        { input: "https://www.wired.com/review/volvo-ex-90/", type: "url" },
        { input: "https://www.digitaltrends.com/cars/volvo-ex90-vs-rivian-r1s-can-volvo-take-out-the-king-of-electric-suvs/", type: "url" },
        { input: "https://practicapp.com/carbagepilot-part1/", type: "url" },
        { input: "https://www.digitaltrends.com/cars/volvo-ex90-vs-tesla-model-y-is-teslas-cheaper-ev-also-better/", type: "url" },
        { input: "http://www.muyinteresante.com/actualidad/el-suv-hibrido-insignia-de-volvo-mejor-que-nunca.html", type: "url" },
        { input: "data.json", type: "json" },
        { input: "", type: "text" },
    ];

    await processAllSources(inputs);
})();
