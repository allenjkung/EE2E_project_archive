import React, { useState } from 'react';

import UserList from './UserList';
import Messages from './Messages';

import './Styles.css';

function MainMenu() {
  const [messageWith, setMessageWith] = useState<String>('');

  if (messageWith === '') {
    return (
      <div className="user-box">
        <UserList setMessageWith={setMessageWith} />
      </div>
    );
  }
  return (
    <div className="main-menu">
      <div className="user-box">
        <UserList setMessageWith={setMessageWith} />
      </div>
      <div className="message-box">
        <Messages messageWith={messageWith} />
      </div>
    </div>
  );
}

export default MainMenu;
