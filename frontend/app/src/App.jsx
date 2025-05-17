import { useState, useEffect } from 'react'
import 'reactjs-popup/dist/index.css';
import './App.css'

import PlantTable from './components/greenhouse/PlantTable';
import { AddPlant } from './components/Interacts';

function App() {
  const [plants, setPlants] = useState([]);

  useEffect(() => {
    fetch('/api/greenhouse')
      .then(res => res.json())
      .then(data => setPlants(data));
  }, []);

  return (
    <div>
      <AddPlant />
      <PlantTable plants = {plants} />
    </div>
);
}

export default App
