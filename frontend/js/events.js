//HAMMOUD Abdellah
// Fonction pour gérer le clic sur le bouton "Buy"
document.addEventListener("DOMContentLoaded", function() {
  const buyButtons = document.querySelectorAll(".btn");

  buyButtons.forEach(button => {
    button.addEventListener("click", function() {
      const product = this.getAttribute("data-product");
      const price = parseFloat(this.getAttribute("data-price"));
      const quantity = parseInt(document.getElementById(`quantity${this.id.replace('buyButton', '')}`).value);
      const page = window.location.pathname.includes("watches") ? "watches" : "home";
      // console.log(product);

      // Vérification de la quantité
      if (quantity < 1) {
        alert("La quantité doit être supérieure ou égale à 1.");
        return;
      }

      const totalPrice = price * quantity;
      // console.log(product + "|" + price + "|" + quantity + "|" + page )

      // Envoi de l'événement d'achat au backend
      fetch('http://localhost:3000/log-purchase', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product, quantity, price: totalPrice, page })
      })
      .then(response => response.json())
      .then(data => {
        console.log('Réponse du backend:', data)
      })
      .catch(error => {
        console.error('Erreur:', error)
      });
    });
  });
});


