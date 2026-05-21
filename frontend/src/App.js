import React, { useEffect, useState } from 'react';
import { MapContainer, Marker, Popup, Rectangle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';


// 1. PETIT CORRECTIF OBLIGATOIRE POUR LES ICÔNES LEAFLET DANS REACT
// Par défaut, React a du mal à charger les images des marqueurs Leaflet.
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

function App() {

  const customIcon = new L.Icon({
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],           // Taille standard de l'icône
    iconAnchor: [12, 41],         // C'EST CETTE LIGNE : On ancre la pointe tout en bas au centre
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  const [positions, setPositions] = useState([]);

  // 2. DÉFINITION DES DIMENSIONS DE TON BUREAU (En centimètres)
  // On imagine un bureau qui fait 120 cm de largeur et 80 cm de hauteur.
  // Le format Leaflet pour les limites (bounds) est : [[Y_min, X_min], [Y_max, X_max]]
  const bureauBounds = [[0, 0], [80, 120]];

  // 3. ÉCOUTE DU WEBSOCKET (Ton Mac)
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = (event) => {
      const response = JSON.parse(event.data);
      // Supposons que le serveur envoie : { "data": [{"id": 1, "x": 45.2, "y": 30.1, "confidence": 0.95}] }
      setPositions(response.data);
    };

    return () => ws.close();
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h2>🖥️ Interface Digital Twin — Mode Bureau Virtuel</h2>
      <p>Les coordonnées s'affichent en centimètres (Origine [0,0] en bas à gauche).</p>

      {/* 4. LE CONTENEUR DE LA CARTE */}
      <MapContainer 
        crs={L.CRS.Simple}        // TRÈS IMPORTANT : Active le mode 2D plat (pas de globe terrestre)
        bounds={bureauBounds}     // Centre la vue sur les limites du bureau
        maxZoom={2}               // Empêche de zoomer à l'infini dans le vide
        minZoom={-1}              // Permet de dézoomer un peu pour voir tout le bureau
        style={{ height: "600px", width: "900px", background: "#ecf0f1", borderRadius: "8px" }}
      >
        
        {/* 5. LE RECTANGLE QUI SIMULE LE SURFACE DU BUREAU */}
        {/* En attendant la photo, ce rectangle blanc matérialise l'espace de travail */}
        <Rectangle 
          bounds={bureauBounds} 
          pathOptions={{ 
            color: '#2c3e50',      // Couleur de la bordure du bureau
            weight: 3, 
            fillColor: '#ffffff',  // Couleur du fond du bureau
            fillOpacity: 1 
          }} 
        />

        {/* 6. AFFICHAGE DES MARQUEURS EN TEMPS RÉEL */}
        {positions.map((objet) => (
          <Marker 
            key={objet.id} 
            // ATTENTION : Leaflet prend l'ordre [Axe_Vertical, Axe_Horizontal], donc [y, x]
            position={[objet.y, objet.x]}
            icon={customIcon}
          >
            <Popup>
              <strong>📦 Objet ID: {objet.id}</strong> <br />
              Position : {objet.x}cm , {objet.y}cm <br />
              Confiance : {Math.round(objet.confidence * 100)}%
            </Popup>
          </Marker>
        ))}

      </MapContainer>
    </div>
  );
}

export default App;