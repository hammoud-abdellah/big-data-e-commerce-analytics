//HAMMOUD Abdellah
const express = require("express");
const fs = require("fs");
const cors = require("cors");
const path = require("path");
const app = express();
const port = 3000;

// Configuration CORS
app.use(
  cors({
    origin: "http://127.0.0.1:5500", 
    methods: ["GET", "POST"], 
    allowedHeaders: ["Content-Type"],
  })
);

// Middleware pour analyser les requêtes JSON
app.use(express.json());

// Variables globales pour le fichier courant et son dernier timestamp
let currentLogFile = null;
let lastLogTimestamp = null;
let nextFileTime = null; 

const generateRandomInterval = () => {
  const min = 2 * 60 * 1000;
  const max = (2 * 60 + 59) * 1000; 
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

// Fonction pour créer ou réutiliser un fichier de log
const createLogFile = (product, quantity, price, page) => {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  const hour = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const seconds = String(now.getSeconds()).padStart(2, "0");

  // Créer le répertoire pour l'heure
  const logDir = path.join(__dirname, "logs", `${year}${month}${day}${hour}`);
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }

  // Construire le nom du fichier basé sur l'horodatage
  const timestamp = `${year}${month}${day}${hour}${minutes}${seconds}`;
  const logFilePath = path.join(logDir, `${timestamp}.txt`);

  // Vérifier si un nouveau fichier est nécessaire
  if (!lastLogTimestamp || !nextFileTime || now - lastLogTimestamp > nextFileTime) {
    currentLogFile = logFilePath;
    lastLogTimestamp = now;
    nextFileTime = generateRandomInterval(); // Générer une nouvelle durée aléatoire
  }

  // Construire le message de log
  const logMessage = `${year}/${month}/${day} ${hour}:${minutes}:${seconds} | ${product} | ${quantity} | ${price} | ${page}\n`;

  // Écrire le message dans le fichier
  fs.appendFileSync(currentLogFile, logMessage);
};

// Route pour enregistrer un événement d'achat
app.post("/log-purchase", (req, res) => {
  try {
    const { product, quantity, price, page } = req.body;

    if (!product || !quantity || !price || !page) {
      return res.status(400).send("Données invalides");
    }

    console.log(`Produit: ${product}, Quantité: ${quantity}, Prix: ${price}, Page: ${page}`);
    // Appeler la fonction pour gérer le fichier log
    createLogFile(product, quantity, price, page);

    res.status(200).send("Achat enregistré");
  } catch (error) {
    console.error("Erreur serveur:", error);
    res.status(500).send("Erreur serveur");
  }
});

// Lancer le serveur
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
