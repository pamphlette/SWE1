import Popup from 'reactjs-popup';
import React, { useState, useEffect } from 'react';
import 'reactjs-popup/dist/index.css';
import { RiDeleteBinFill } from "react-icons/ri";
import { MdModeEdit } from "react-icons/md";

function Button({ text }) {
    return (
      <button>{text}</button>
    );
  }

// del plant button
function DelPlant ({ plantID }) {
  // grab the id of the plant being deleted
  const handleDelete = () => {
      fetch('/api/delete-plant', {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: plantID }) 
    })
  // if you fail to delete the plant for some reason...
  .then(res => {
    return res.json().then(data => {
      if (!res.ok) {
        throw new Error("failed to delete plant");
      }
      return data;
    });
  })
    .then(data => {
      console.log("Plant deleted:", data);
      //if (onDelete) onDelete(plantID);      // optional callback to refresh UI
    })
    .catch(err => console.error(err));
  };

  return (
      <button onClick = {handleDelete}>
        <RiDeleteBinFill color = "grey"/>
      </button>
  );
}

// add plant modal
function AddPlant() {
  // Set up the variables that are going to be changed
  const [genus, setGenus] = useState('');
  const [species, setSpecies] = useState('');
  const [statusID, setStatusID] = useState('');
  const [qty, setQty] = useState(0);
  const [wishlist, setWishlist] = useState(0);
  const [statuses, setStatuses] = useState([]);

  // fetch status right away
    useEffect(() => {
    fetch('/api/statuses')
      .then(res => res.json())
      .then(data => setStatuses(data))
      .catch(err => console.error("Error fetching statuses", err));
  }, []);

  // handling form submission
  const handleSubmit = (e, close) => {
    e.preventDefault();
    const newPlant = { genus, species, statusID, qty, wishlist };

    // route info...
    fetch('/api/add-plant', {
      method: 'POST',
      headers: {'Content-Type' : 'application/json'},
      body: JSON.stringify(newPlant)
    })
    // if you fail to add the plant for some reason...
    .then(res => {
      if (!res.ok) throw new Error("failed to add plant");
      return res.json();
    })
    // if good, print results
    .then(data => {
        console.log('Plant added:', data);
        close(); 
    });
  };

  return (
    <div>

      <Popup trigger={<button>add a plant</button>} modal nested>
        {(close) => (
          <div className="modal" >
            <div className="modal-content">
              <h3>Add a plant</h3>
              <form onSubmit={(e) => handleSubmit(e, close)}>
                <label>Genus:<input value={genus} onChange={e => setGenus(e.target.value)} /></label><br/>
                <label>Species:<input value={species} onChange={e => setSpecies(e.target.value)} /></label><br/>
                <label>Status:
                <select value={statusID} onChange={e => setStatusID(e.target.value)}>
                  <option value="">-- Select Status --</option>
                  {statuses.map((s) => (
                    <option key={s.statusID} value={s.statusID}>{s.status}</option>
                  ))}
                  </select>
                </label><br/>
                <label>Quantity: <input type="number" value={qty} onChange={e => setQty(Number(e.target.value))} min="0" /></label><br/>
                <label>Wishlist: <input type="checkbox" checked={wishlist === 1} onChange={e => setWishlist(e.target.checked ? 1 : 0)} /></label><br/>
                <button type="submit">Add Plant</button>
              </form>
            </div>
          </div>
        )}
      </Popup>
      
    </div>
  );
}

// edit plant modal
function EditPlant({ plant }) {
  // Set up the variables that are going to be changed
  const [genus, setGenus] = useState(plant.genus);
  const [species, setSpecies] = useState(plant.species);
  const [statusID, setStatusID] = useState(plant.statusID || '');
  const [qty, setQty] = useState(plant.qty);
  const [wishlist, setWishlist] = useState(plant.wishlist);
  const [statuses, setStatuses] = useState([]);

  // Update plant that will be changed...
    useEffect(() => {
    setGenus(plant.genus);
    setSpecies(plant.species);
    setStatusID(plant.statusID || '');
    setQty(plant.qty);
    setWishlist(plant.wishlist);
  }, [plant]);

  // get statuses
  useEffect(() => {
    fetch('/api/statuses')
      .then(res => res.json())
      .then(data => setStatuses(data))
      .catch(err => console.error("Error fetching statuses", err));
  }, []);

  const handleSubmit = (e, close) => {
    e.preventDefault();

    // making a new plant object...
    const updatedPlant = {
      plantID: plant.plantID,
      genus, species, statusID, qty, wishlist
    };

    // route info...
    fetch('/api/edit-plant', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updatedPlant)
    })
      .then(res => {
        return res.json().then(data => {
          if (!res.ok) throw new Error(data);
          return data;
        });
      })
      .then(data => {
        console.log('Plant edited:', data);
        close(); 
      });
  };

  return (
    <div>

      <Popup trigger={<MdModeEdit color = 'grey'/>} modal nested>
        {(close) => (
          <div className="modal" >
            <div className="modal-content">
              <h3>Edit plant</h3>
              <form onSubmit={(e) => handleSubmit(e, close)}>
                <label>Genus: <input value={genus} onChange={e => setGenus(e.target.value)} required /></label><br/>
                <label>Species: <input value={species} onChange={e => setSpecies(e.target.value)} required /></label><br/>
                <label>Status:
                  <select value={statusID} onChange={e => setStatusID(e.target.value)}>
                  <option value="">-- Select Status --</option>
                  {statuses.map((s) => (
                    <option key={s.statusID} value={s.statusID}>{s.status}</option>
                  ))}
                </select>
              </label><br/>
              <label>Quantity: <input type="number" value={qty} onChange={e => setQty(Number(e.target.value))} min="0" /></label><br/>
              <label>Wishlist: <input type="checkbox" checked={wishlist === 1} onChange={e => setWishlist(e.target.checked ? 1 : 0)} /></label><br/>
              <button type="submit">Save Changes</button>
              </form>
            </div>
          </div>
        )}
      </Popup>
      
    </div>
  );
}

export {Button, AddPlant, DelPlant, EditPlant};