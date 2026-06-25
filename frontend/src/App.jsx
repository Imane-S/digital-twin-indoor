import React, { useEffect, useState } from 'react';
import { MapContainer, ImageOverlay, Rectangle, Tooltip } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './App.css';

const bounds = [[0, 0], [47, 98]]; 
const urlPlan = "https://upload.wikimedia.org/wikipedia/commons/9/9a/Sample_Floorplan.png";

function App() {
  const [zoneAStatus, setZoneAStatus] = useState("Vide");
  const [zoneBStatus, setZoneBStatus] = useState("Vide");
  const [history, setHistory] = useState([]);

  useEffect(() => {
    // Fonction qui va chercher les données sur le port 8080
    const fetchStatusAndHistory = async () => {
      try {
        const res = await fetch("http://localhost:8080/history");
        const data = await res.json();
        
        // Mettre à jour l'historique dans le tableau
        setHistory(data);

        if (data && data.length > 0) {
          // Trouver la ligne la plus récente pour la Zone A et la Zone B
          const dernierA = data.find(item => item.zone === "Zone_A");
          const dernierB = data.find(item => item.zone === "Zone_B");

          // Mettre à jour l'état des rectangles sur la carte
          if (dernierA) setZoneAStatus(dernierA.statut);
          if (dernierB) setZoneBStatus(dernierB.statut);
        }
      } catch (err) {
        console.error("⚠️ Erreur lors de la récupération des données:", err);
      }
    };

    // Charger les données immédiatement au démarrage
    fetchStatusAndHistory();

    // Re-vérifier automatiquement TOUTES les secondes (1000ms)
    const interval = setInterval(fetchStatusAndHistory, 1000);

    // Nettoyer l'intervalle si on quitte l'application
    return () => clearInterval(interval);
  }, []);

  const coordZoneA = [[5, 5], [42, 45]];   
  const coordZoneB = [[5, 53], [42, 93]];  

  const obtenirStyle = (status) => ({
    color: status === "Present" ? "#ff4d4d" : "#2ecc71",
    fillColor: status === "Present" ? "#ff4d4d" : "#2ecc71",
    fillOpacity: 0.4,
    weight: 3
  });

  const formaterDate = (isoString) => {
    const d = new Date(isoString);
    return d.toLocaleTimeString('fr-FR') + " " + d.toLocaleDateString('fr-FR');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>📊 Jumeau Numérique – Mon Bureau</h1>
        <p>Statut des emplacements synchronisé en temps réel</p>
      </header>

      <div className="map-container-wrapper" style={{ display: 'flex', justifyContent: 'center', padding: '20px' }}>
        <MapContainer 
          crs={L.CRS.Simple} 
          bounds={bounds} 
          style={{ height: "400px", width: "700px", borderRadius: "8px", boxShadow: "0 4px 12px rgba(0,0,0,0.1)" }}
        >
          <ImageOverlay url={urlPlan} bounds={bounds} />

          <Rectangle bounds={coordZoneA} pathOptions={obtenirStyle(zoneAStatus)}>
            <Tooltip permanent direction="center" className="zone-tooltip">
              <strong>Zone A</strong> <br /> {zoneAStatus === "Present" ? "🔴 Occupé" : "🟢 Vide"}
            </Tooltip>
          </Rectangle>

          <Rectangle bounds={coordZoneB} pathOptions={obtenirStyle(zoneBStatus)}>
            <Tooltip permanent direction="center" className="zone-tooltip">
              <strong>Zone B</strong> <br /> {zoneBStatus === "Present" ? "🔴 Occupé" : "🟢 Vide"}
            </Tooltip>
          </Rectangle>
        </MapContainer>
      </div>

      <div className="dashboard-status" style={{ display: 'flex', justifyContent: 'center', gap: '40px', marginTop: '10px' }}>
        <div className={`status-card ${zoneAStatus}`}><h3>Zone A: {zoneAStatus}</h3></div>
        <div className={`status-card ${zoneBStatus}`}><h3>Zone B: {zoneBStatus}</h3></div>
      </div>

      <div className="history-section" style={{ maxWidth: '800px', margin: '40px auto', padding: '0 20px' }}>
        <h2>📜 Historique des Détections</h2>
        <div style={{ maxHeight: '250px', overflowY: 'auto', border: '1px solid #ddd', borderRadius: '8px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead style={{ backgroundColor: '#f5f5f5', position: 'sticky', top: 0 }}>
              <tr>
                <th style={{ padding: '12px', borderBottom: '2px solid #ddd' }}>Zone</th>
                <th style={{ padding: '12px', borderBottom: '2px solid #ddd' }}>Statut</th>
                <th style={{ padding: '12px', borderBottom: '2px solid #ddd' }}>Horodatage</th>
              </tr>
            </thead>
            <tbody>
              {history.length === 0 ? (
                <tr>
                  <td colSpan="3" style={{ padding: '12px', textAlign: 'center', color: '#777' }}>Aucun historique disponible</td>
                </tr>
              ) : (
                history.map((record) => (
                  <tr key={record.id} style={{ borderBottom: '1px solid #eee' }}>
                    <td style={{ padding: '12px' }}><strong>{record.zone === "Zone_A" ? "Zone A" : "Zone B"}</strong></td>
                    <td style={{ padding: '12px' }}>
                      <span style={{
                        padding: '4px 8px',
                        borderRadius: '4px',
                        backgroundColor: record.statut === "Present" ? "#ffebee" : "#e8f5e9",
                        color: record.statut === "Present" ? "#c62828" : "#2e7d32",
                        fontWeight: 'bold'
                      }}>
                        {record.statut === "Present" ? "Occupé" : "Vide"}
                      </span>
                    </td>
                    <td style={{ padding: '12px', color: '#555' }}>{formaterDate(record.timestamp)}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default App;