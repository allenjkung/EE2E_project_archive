import React, { useState } from 'react';
import forge from 'node-forge';

import { Button, TextField } from '@material-ui/core';

type Message = {
  id: number,
  username_from: String,
  message: String
};

interface Props {
  messageTo: String;
  setMessages: (messages: Array<Message>) => void;
}

function TextBox(props: Props) {
  const { messageTo, setMessages } = props;
  const [message, setMessage] = useState('');
  function sendMessage(value) {
    fetch('/api/getpublic', {
      method: 'POST',
      headers: new Headers({ 'content-type': 'application/json' }),
      mode: 'no-cors',
      body: JSON.stringify({
        to: messageTo,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        const publicKeySelf = forge.pki.publicKeyFromPem(data.public_key_self);
        const publicKeyUser = forge.pki.publicKeyFromPem(data.public_key_user);
        const encryptedSelf = publicKeySelf.encrypt(value);
        const encryptedUser = publicKeyUser.encrypt(value);
        fetch('/api/message/input', {
          method: 'POST',
          headers: new Headers({ 'content-type': 'application/json' }),
          mode: 'no-cors',
          body: JSON.stringify({
            to: messageTo,
            message_self: encryptedSelf,
            message_to: encryptedUser,
          }),
        })
          .then((nRes) => nRes.json())
          .then((nData) => {
            fetch('/api/getkey')
              .then((keyRes) => keyRes.json())
              .then((keyData) => {
                if (data.success) {
                  const privateEncrypted = forge.pki.privateKeyFromPem(keyData.private);
                  const tarray: Message[] = [];
                  for (let i = 0; i < nData.messages.length; i += 1) {
                    tarray.push({
                      id: nData.messages[i].id,
                      username_from: nData.messages[i].username_from,
                      message: privateEncrypted.decrypt(nData.messages[i].message),
                    });
                  }
                  setMessages(tarray);
                }
              });
          });
      })
      .catch((error) => {
        <div className="login-error-box">
          Malformed message was recieved:
          {error}
        </div>;
      });
  }
  function handleButton() {
    sendMessage(message);
    setMessage('');
  }
  function handleKeyUp(event) {
    if (event.key === 'Enter') {
      sendMessage(message);
      setMessage('');
    }
  }
  function handleInput(event) {
    const { value: newValue } = event.target;
    setMessage(newValue);
  }
  return (
    <div className="message-menu">
      <TextField type="text" className="message-input" value={message} onKeyUp={handleKeyUp} onChange={handleInput} />
      <Button type="button" className="message-button" value="Enter" onClick={handleButton}>
        Enter
      </Button>
    </div>
  );
}

export default TextBox;
