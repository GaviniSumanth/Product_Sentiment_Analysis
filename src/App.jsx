import { Tab } from "@headlessui/react";
import "./style.css";
import Card from "./components/Card";
function App() {
  return (
    <>
      <Landing />
      <div className="tabs">
        <Card
          src="https://images.unsplash.com/photo-1543286386-713bdd548da4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80"
          description="The Flipkart Product Sentiment Analysis project aims to build a
        powerful natural language processing (NLP) model that can analyze
        customer sentiments based on product reviews from Flipkart, one of
        India's leading online marketplaces and tell whether a cetain product is worth buying or not."
          url="Form?form=product_sentiment_analysis"
        />
      </div>
    </>
  );
}

function Landing() {
  return (
    <div id="Landing">
      <div className="ripple-background">
        <div className="circle xxlarge"></div>
        <div className="circle xlarge"></div>
        <div className="circle large"></div>
        <div className="circle medium"></div>
        <div className="circle small"></div>
        <h1 id="Title">Internship</h1>
        <h1 id="Title">Project</h1>
        <p id="Description">
          The Flipkart Product Sentiment Analysis project aims to build a
          powerful natural language processing (NLP) model that can analyze
          customer sentiments based on product reviews from Flipkart, one of
          India's leading online marketplaces.
        </p>
      </div>
    </div>
  );
}

export default App;
