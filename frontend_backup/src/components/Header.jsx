const Header = () => {
  return (
    <header className="top-header">
      <div>
        <h1 className="page-title">Melofy</h1>
        <p className="page-subtitle">Discover free tracks from Jamendo</p>
      </div>

      <div className="user-pill">
        <div className="user-avatar">M</div>
        <span className="user-name">Guest</span>
      </div>
    </header>
  );
};

export default Header;
