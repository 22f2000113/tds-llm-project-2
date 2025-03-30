// hash.js
// Access Web Crypto API in Node.js
async function hash(text) {
    const encoder = new TextEncoder();
    const data = encoder.encode(text);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
    return hashHex;
}

// To call this function from the command line
async function main() {
    const text = process.argv[2];
    const parsedJson = JSON.parse(text);
    const hashed = await hash(JSON.stringify(parsedJson));
    console.log(hashed);  // Output the hash to the console
}

main();
