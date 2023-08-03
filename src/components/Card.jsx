import { Link } from "react-router-dom";
function Card(props) {
  return (
    <div className="card">
      <img src={props.src} className="card-image" />
      <div className="card-description">
        {props.description.length > 450
          ? props.description.slice(0, 450) + "..."
          : props.description}
      </div>
      <Link to={props.url} className="button card-button">
        Open
      </Link>
    </div>
  );
}
export default Card;
