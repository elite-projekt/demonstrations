import { useEffect, useState } from 'react';
import './App.css';
import './elite.css';
import './bootstrap.min.css';

import wifi_list from './assets/wifi_list.png';
import privacy_combined from './assets/privacy_combined.png';
import nimbus_connect from './assets/nimbus_connect.png';
import notification from './assets/notification.png';
import disclaimer from './assets/disclaimer.png';


enum AppState {
  WAITING_TRANSLATION,
  DEVICE_SELECTION,
  DEVICE_OWN,
  DEVICE_PROVIDED
}


interface ManualEntry {
  heading: string,
  text: string,
  image: string,
}

interface TranslationMap {
  [key: string]: string;
}

function Manual() {
  const [translations, setTranslations] = useState<TranslationMap>({});
  const [currentState, setCurrentState] = useState<AppState>(AppState.DEVICE_SELECTION);


  useEffect(() => {
    async function getTranslations() {
      const response = await fetch('http://127.0.0.1:5000/orchestration/data/demo/uhh_evil_twin/translations');
      const json = await response.json();
      console.log(json);
      setTranslations(json.translations);
    }
    getTranslations();
  },[]);

  useEffect(() => {
    if(translations !== null) {
      setCurrentState(AppState.DEVICE_SELECTION);
    }
  }, [translations]);

  function handleOwnButton() {
    setCurrentState(AppState.DEVICE_OWN);
  }

  function handleProvidedButton() {
    setCurrentState(AppState.DEVICE_PROVIDED);
  }
  let own_device_manual: ManualEntry[] = [];

  if(currentState !== AppState.WAITING_TRANSLATION && translations !== null) {
  own_device_manual = [
    {
      "heading": translations["uhh_evil_twin_step_one_heading"],
      "text": translations["uhh_evil_twin_step_one_text"],
      "image": wifi_list
    },
    {
      "heading": translations["uhh_evil_twin_step_two_heading"],
      "text": translations["uhh_evil_twin_step_two_text"],
      "image": privacy_combined
    },
    {
      "heading": translations["uhh_evil_twin_step_three_heading"],
      "text": translations["uhh_evil_twin_step_three_text"],
      "image": nimbus_connect
    },
    {
      "heading": translations["uhh_evil_twin_step_four_heading"],
      "text": translations["uhh_evil_twin_step_four_text"],
      "image": notification
    },
    {
      "heading": translations["uhh_evil_twin_step_five_heading"],
      "text": translations["uhh_evil_twin_step_five_text"],
      "image": disclaimer
    },
  ];
  }

  switch (currentState) {
    case AppState.WAITING_TRANSLATION:
      return (<div>Loading data...</div>);
    case AppState.DEVICE_SELECTION:
      return (
        <div>
          <h2> { translations["uhh_evil_twin_heading"] } </h2>
          <p> { translations["uhh_evil_twin_text"] } </p>
          <div>
            <button type="button" onClick={handleOwnButton}> { translations["uhh_evil_own_device_button"] } </button>
            <button type="button" onClick={handleProvidedButton}> { translations["uhh_evil_provided_device_button"] } </button>
          </div>
        </div>);
    case AppState.DEVICE_OWN:
      return (
      <div>
      { own_device_manual.map((item) => {
        return(
          <div className='manual-entry'>
            <h2> {item.heading} </h2>
            <div className='manual-content'>
              { item.text && <p> { item.text } </p> }
              <img src={item.image} alt="Cool image" />
            </div>
          </div>
          );
      })
      }
        <button type="button" onClick={handleProvidedButton}> { translations["uhh_evil_manual_button"] } </button>
      </div>
      );
    case AppState.DEVICE_PROVIDED:
      return (
      <div>
        <div>
          <h2> { translations["uhh_evil_twin_begin_heading"] } </h2>
          <p> { translations["uhh_evil_twin_begin_text"] } </p>
        </div>
      </div>
      );
  }
}

function App() {
  return (
  <div>
    <Manual />
  </div>
  );
}

export default App;
