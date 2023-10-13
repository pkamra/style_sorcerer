<template>
  <div id="app">
      <h1 class="orange-label">Enchanted Masquerade: Spooky Costume Generator</h1>
      <div class="input-container">
      <label class="orange-label" for="prompt">Enter your prompt:</label>
      <textarea v-model="prompt" id="prompt" placeholder="Enter your prompt"></textarea>
    </div>
    <div class="input-container">
      <label class="orange-label" for="stylePreset">Select style:</label>
      <select v-model="stylePreset">
          <option value="photographic">Photographic</option>
          <option value="digital-art">Digital Art</option>
          <option value="cinematic">Cinematic</option>
          <option value="anime">Anime</option>
          <option value="neon-punk">Neon Punk</option>
          <option value="3d-model">3D Model</option>
          <option value="enhance">Enhance</option>
          <option value="fantasy-art">3D Model</option>
          <option value="comic-book">Comic Book</option>
          <option value="origami">Origami</option>
          <option value="photographic">Photographic</option>
      <!-- Add more style presets as needed -->
      </select>
    </div>
    <div class="input-container">
      <label class="orange-label" for="numImages">Number of Images:</label>
      <select id="numImages" v-model="num_images">
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5">5</option>
        <option value="6">6</option>
        <option value="7">7</option>
        <option value="8">8</option>
        <option value="9">9</option>
        <option value="10">10</option>
        <!-- Add more options as needed -->
      </select>
    </div>

    <button @click="generateCostumes">Generate Costumes</button>
    <div v-if="costumesGenerated">
        <div class="costumes-grid"> 
          <div v-for="(imageData, index) in image_data_list" :key="index" class="costume-item">
            <img :src="imageData" alt="Recommended Costume" />
          </div>
        </div>
    </div>
  </div>
</template>
  
<script>
  import axios from 'axios';
  export default {
    data() {
      return {
        prompt: '',
        image_data_list: [],
        stylePreset: 'neon-punk',
        costumesGenerated: false,
        num_images: 1,
      };
    },
    methods: {
      generateCostumes() {
        // Send the prompt to the backend API and get the generated costume
        // Update this method to make an API request to your backend
        // Set this.generatedCostume with the response from the backend API
        // For example:
        axios.post('http://localhost:5000/generate_images', { 
          prompt: this.prompt , 
          style_preset: this.stylePreset ,
          num_images:parseInt(this.num_images)
        })
          .then(response => {
            // Assuming response.data.image_data_list is an array of base64 image strings
            this.image_data_list = response.data.image_data_list.map(data => 'data:image/png;base64,' + data);
            this.costumesGenerated = true;
            console.log(this.image_data_list);
          });
      },
    },
  };
  </script>
  
<style>

html, body {
  height: 100%;
  margin: 0;
  background-color: black;
  color: white;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.input-container {
  margin: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

textarea, select {
  margin-top: 8px;
  padding: 8px;
  font-size: 16px;
}

button {
  margin-top: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
  padding: 10px 20px;
  font-size: 18px;
}

button:hover {
  background-color: #45a049;
}

.costumes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
  gap: 20px;
}

.costume-item img {
  width: 100%;
  height: auto;
}

.orange-label {
  color: #FFA500; /* Set label text color to orange */
  font-size: 18px; /* Set font size to 18 pixels, adjust as needed */
}
</style>
  