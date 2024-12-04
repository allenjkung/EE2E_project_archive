import React, { useState } from 'react';
import forge from 'node-forge';
import { Paper, Typography } from '@material-ui/core';

import './Styles.css';

import TextBox from './TextBox';

type Message = {
  id: number,
  username_from: String,
  message: String
};

interface Props {
  messageWith: String;
}

function Messages(props: Props) {
  const [currentWith, setCurrentWith] = useState<String>('');
  const [messages, setMessages] = useState<Array<Message>>([]);
  const [eMessage, setEMessage] = useState('');
  const { messageWith } = props;
  if (messageWith !== currentWith && messageWith !== '') {
    setCurrentWith(messageWith);
    fetch('/api/getkey')
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          const privateEncrypted = forge.pki.privateKeyFromPem(data.private);
          fetch('/api/message', {
            method: 'POST',
            headers: new Headers({ 'content-type': 'application/json' }),
            mode: 'no-cors',
            body: JSON.stringify({
              to: messageWith,
            }),
          })
            .then((nRes) => nRes.json())
            .then((nData) => {
              if (nData.success === false) {
                setMessages([]);
              } else {
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
            })
            .catch((error) => {
              <div className="login-error-box">
                Malformed message was recieved:
                {error}
              </div>;
            });
        } else {
          setEMessage(data.message);
        }
      })
      .catch((error) => {
        <div className="login-error-box">
          Malformed message was recieved:
          {error}
        </div>;
      });
  }
  return (
    <Paper className="messages">
      <Typography variant="h6">{messageWith}</Typography>
      <hr />
      {messages.map((row, index) => (
        <div className="message-section" key={row.id} tabIndex={index}>
          <div className="message-username">
            {row.username_from}
            :
          </div>
          <div className="message-content">{row.message}</div>
        </div>
      ))}
      <TextBox messageTo={messageWith} setMessages={setMessages} />
      <div>{eMessage}</div>
    </Paper>
  );
}

export default Messages;
