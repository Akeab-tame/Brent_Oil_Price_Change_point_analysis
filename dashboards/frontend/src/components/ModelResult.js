// frontend/src/components/ModelResult.js

import React from 'react';
import { Card, Row, Col } from 'react-bootstrap';
import PropTypes from 'prop-types';
import './ModelResult.css';

const ModelResult = ({ modelData }) => {
    if (!modelData) return null;

    return (
        <Card className="model-result-card">
            <Card.Body>
                <Card.Title>Model Analysis Results</Card.Title>
                <Row>
                    <Col md={6}>
                        <p><strong>Prediction Accuracy:</strong> {modelData.accuracy}%</p>
                        <p><strong>Mean Squared Error:</strong> {modelData.mse}</p>
                    </Col>
                    <Col md={6}>
                        <p><strong>Forecasted Price:</strong> ${modelData.forecastPrice}</p>
                        <p><strong>Confidence Interval:</strong> {modelData.confidenceInterval}</p>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    );
};

ModelResult.propTypes = {
    modelData: PropTypes.shape({
        accuracy: PropTypes.number,
        mse: PropTypes.number,
        forecastPrice: PropTypes.number,
        confidenceInterval: PropTypes.string
    })
};

export default ModelResult;