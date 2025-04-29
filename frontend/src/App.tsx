import React, { useState } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  Slider, 
  Select, 
  MenuItem, 
  FormControl, 
  InputLabel,
  Button,
  Paper
} from '@mui/material';
import './App.css';

function App() {
  const [style, setStyle] = useState('hard_tech');
  const [pitch, setPitch] = useState(1.0);
  const [tailLength, setTailLength] = useState(0.5);
  const [punch, setPunch] = useState(0.7);
  const [saturation, setSaturation] = useState(0.5);
  const [compression, setCompression] = useState(0.3);
  const [generatedKick, setGeneratedKick] = useState<string | null>(null);

  const handleGenerate = async () => {
    try {
      const response = await fetch('http://localhost:8000/generate-kick', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          style,
          pitch,
          tail_length: tailLength,
          punch,
          saturation,
          compression
        }),
      });
      
      const data = await response.json();
      setGeneratedKick(data.audio_url);
    } catch (error) {
      console.error('Error generating kick:', error);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Kick Generator AI
        </Typography>
        
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel>Style</InputLabel>
            <Select
              value={style}
              label="Style"
              onChange={(e) => setStyle(e.target.value)}
            >
              <MenuItem value="hard_tech">Hard Tech</MenuItem>
              <MenuItem value="frenchcore">Frenchcore</MenuItem>
              <MenuItem value="psy_trance">Psy Trance</MenuItem>
            </Select>
          </FormControl>

          <Typography gutterBottom>Pitch</Typography>
          <Slider
            value={pitch}
            onChange={(_, value) => setPitch(value as number)}
            min={0.5}
            max={2.0}
            step={0.1}
            valueLabelDisplay="auto"
          />

          <Typography gutterBottom>Tail Length</Typography>
          <Slider
            value={tailLength}
            onChange={(_, value) => setTailLength(value as number)}
            min={0.1}
            max={1.0}
            step={0.1}
            valueLabelDisplay="auto"
          />

          <Typography gutterBottom>Punch</Typography>
          <Slider
            value={punch}
            onChange={(_, value) => setPunch(value as number)}
            min={0.1}
            max={1.0}
            step={0.1}
            valueLabelDisplay="auto"
          />

          <Typography gutterBottom>Saturation</Typography>
          <Slider
            value={saturation}
            onChange={(_, value) => setSaturation(value as number)}
            min={0.1}
            max={1.0}
            step={0.1}
            valueLabelDisplay="auto"
          />

          <Typography gutterBottom>Compression</Typography>
          <Slider
            value={compression}
            onChange={(_, value) => setCompression(value as number)}
            min={0.1}
            max={1.0}
            step={0.1}
            valueLabelDisplay="auto"
          />

          <Button 
            variant="contained" 
            color="primary" 
            fullWidth 
            onClick={handleGenerate}
            sx={{ mt: 2 }}
          >
            Generate Kick
          </Button>
        </Paper>

        {generatedKick && (
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Generated Kick
            </Typography>
            <audio controls src={generatedKick} style={{ width: '100%' }} />
            <Button 
              variant="outlined" 
              color="primary" 
              fullWidth 
              sx={{ mt: 2 }}
              href={generatedKick}
              download="generated_kick.wav"
            >
              Download Kick
            </Button>
          </Paper>
        )}
      </Box>
    </Container>
  );
}

export default App; 