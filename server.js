const express = require('express');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');
const app = express();

const port = 3000;


// Middleware Functions
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static('public'));


// root endpoint
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public/html', 'index.html'));
});

async function crawl_webpage() { 
    return new Promise((resolve, reject) => { 
        exec("..\\Scripts\\python ./Backend/Crawl_WebPage.py", (error, stdout, stderr) => { 
            if (error) { 
                console.error(`exec error: ${error}`); 
                reject('Error executing script'); 
            } 
            else { 
                console.log("Reviews Fetched"); 
                resolve(); 
            } 
        }); 
    }); 
} 

async function get_sentiments() { 
    return new Promise((resolve, reject) => { 
        exec('..\\Scripts\\python ./Backend/Get_Sentiment.py', (error, stdout, stderr) => { 
            if (error) { 
                console.error(`exec error: ${error}`); 
                reject('Error executing script'); 
            } 
            else { 
                console.log("Sentiments Generated"); 
                resolve(); 
            } 
        }); 
    }); 
} 

app.post('/', async (req, res) => { 
    const url = req.body.url; 
    fs.writeFile('./url.txt', url, (err) => { 
        if (err) throw err; console.log("URL Fetched"); 
    }); 
    
    try { 
        await crawl_webpage(); 
        await get_sentiments(); 
        
        fs.readFile('sentiments.txt', 'utf8', (err, data) => { 
            if (err) { 
                console.error(`readFile error: ${err}`); 
                return res.status(500).send('Error reading output file'); 
            } 
            res.send(data); 
        }); 
    } 
    catch (error) { 
        res.status(500).send(error); 
    } 
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
