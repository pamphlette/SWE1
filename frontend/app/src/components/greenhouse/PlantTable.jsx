import { DelPlant, EditPlant } from '../Interacts.jsx';

function PlantTable ({ plants }) {
    return (
        <table>
            <thead>
                <tr>
                    <th></th>
                    <th>Qty</th>
                    <th>Genus</th>
                    <th>Species</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {plants.map((plant) => (
                    <tr key = {plant.plantID}>
                        <td><div style={{ display: 'flex', gap: '3px' }}>
                            <EditPlant plant={plant} />
                            <DelPlant plantID={plant.plantID} /></div></td>
                        <td>{plant.qty}</td>
                        <td>{plant.genus}</td>
                        <td>{plant.species}</td>
                        <td>{plant.status}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}

export default PlantTable;