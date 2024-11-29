

/***
  /* Styling for the device dropdown and search input */
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content div {
  color: black;
  padding: 7px 3px;
  text-decoration: none;
  display: block;
  cursor: pointer;
}

.dropdown-content div:hover {
  background-color: #ddd;
}

.dropdown:hover .dropdown-content {
  display: block;
}


.device-list {
  max-height: 200px;
  overflow-y: auto;
}

/* Add more spacing between the logos */
.header img {
  margin-right: 10px;
}


/* Styling for the search input inside the dropdown */
.search-input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

/* Styling for the search input inside the dropdown */
.search-input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

/* Search results dropdown container */
.search-results {
  max-height: 150px;
  overflow-y: auto;
  background-color: #ffffff;  /* Set background to white */
  border: 1px solid #ccc;  /* Optional: Light border around the search results */
  position: absolute;
  top: 100%;  /* Positioned just below the search input */
  width: 100%;
  z-index: 1;
  box-shadow: none; /* Removed shadow to avoid gray box appearance */
  padding: 0;  /* Ensure no padding creates extra space */
  border-radius: 4px; /* Add border-radius to smooth the corners */
}

/* Individual device item styling */
.device-item {
  padding: 8px 12px;  /* Adjust padding for device item */
  cursor: pointer;
  border-bottom: 1px solid #ddd;  /* Adds a thin separation between items */
  background-color: #fff;  /* Keep background of each device white */
}

/* Hover effect for each device item */
.device-item:hover {
  background-color: #f0f0f0;  /* Light gray background on hover */
}

/* Ensure the last device item does not have a border at the bottom */
.device-item:last-child {
  border-bottom: none;
}
