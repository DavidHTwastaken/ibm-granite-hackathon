import React, {useState, useEffect} from 'react';

export function Main() {

  const [data, setData] = useState([{}]);

  useEffect(() => {
    fetch('/test') // Ensure the backend is running and accessible
      .then((response) => response.json())
      .then((jsonData) => setData(jsonData))
      .catch((error) => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h1>Data from /test</h1>
      <ul>
        {data.map((item) => (
          <li key={item._id}>
            <strong>Name:</strong> {item.name} <br />
            <strong>Gender:</strong> {item.gender} <br />
            <strong>Company:</strong> {item.company} <br />  <br />
          </li>
        ))}
      </ul>
    </div>
  );
}