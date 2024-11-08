// frontend/src/components/Dashboard.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import EventFilter from './EventFilter';
import PriceChart from './PriceChart';
import Statistics from './Statistics';
import DataExport from './DataExport';
import EventImpact from './EventImpact';
import ModelResult from './ModelResult';
import { Container, Row, Col, Tabs, Tab } from 'react-bootstrap';
import './Dashboard.css';

const Dashboard = () => {
    const [getPrices, setPrices] = useState([]);
    const [analysis, setAnalysis] = useState({});
    const [averageYearlyData, setAverageYearlyData] = useState([]);
    const [priceDistributionData, setPriceDistributionData] = useState([]);
    const [startDate, setStartDate] = useState('2023-01-01');
    const [endDate, setEndDate] = useState('2024-01-01');
    const [loading, setLoading] = useState(false);
    const [modelData, setModelData] = useState(null); // State for model results

    // Fetch price data based on selected start and end date
    const fetchPrices = async () => {
        setLoading(true);
        try {
            const priceResponse = await axios.get('http://localhost:5000/api/prices');
            const pricesData = priceResponse.data;
            const formattedData = pricesData.dates.map((date, index) => ({
                dates: date,
                prices: pricesData.prices[index]
            }));
            setPrices(formattedData);
        } catch (error) {
            console.error("Error fetching price trend data:", error);
        } finally {
            setLoading(false);
        }
    };

    // Fetch analysis metrics for statistics display
    const fetchAnalysis = async () => {
        try {
            const analysisResponse = await axios.get('http://localhost:5000/api/analysis-metrics');
            setAnalysis(analysisResponse.data);
        } catch (error) {
            console.error("Error fetching analysis data:", error);
        }
    };

    // Fetch additional data: average yearly prices and price distribution
    const fetchAdditionalData = async () => {
        try {
            const yearlyResponse = await axios.get('http://localhost:5000/api/average-yearly-price');
            const distributionResponse = await axios.get('http://localhost:5000/api/price-distribution');
            setAverageYearlyData(yearlyResponse.data);
            setPriceDistributionData(distributionResponse.data);
        } catch (error) {
            console.error("Error fetching additional analysis data:", error);
        }
    };

    // Fetch model results for ModelResult component
    const fetchModelData = async () => {
        try {
            const modelResponse = await axios.get('http://localhost:5000/api/model-results');
            setModelData(modelResponse.data);
        } catch (error) {
            console.error("Error fetching model results:", error);
        }
    };

    // Fetch all data when component mounts
    useEffect(() => {
        fetchPrices();
        fetchAnalysis();
        fetchAdditionalData();
        fetchModelData();
    }, []);

    return (
        <Container fluid className="dashboard-container">
            {loading && <div className="loading">Loading...</div>}
            <Row className="mb-4">
                <Col>
                    <h2 className="dashboard-title">Brent Oil Price Dashboard</h2>
                    <p className="dashboard-description">
                        Explore how various events have impacted Brent oil prices over time. Use the filters below to narrow down the data, view analysis metrics, and export the results.
                    </p>
                </Col>
            </Row>

            <Tabs defaultActiveKey="statistics" id="dashboard-tabs" className="mb-4">

                {/* Statistics Tab */}
                <Tab eventKey="statistics" title="Statistics">
                    <Row className="mb-4">
                        <Col md={12}>
                            <Statistics analysis={analysis} />
                        </Col>
                    </Row>
                    <Row className="mb-4">
                        <Col>
                            <ModelResult modelData={modelData} /> {/* Display Model Results */}
                        </Col>
                    </Row>
                </Tab>

                {/* Price Trend, Yearly Average, and Distribution Tab */}
                <Tab eventKey="price-trend" title="Time Series Analysis">
                    <Row className="mb-4">
                        <Col>
                            <EventFilter onFilter={(start, end) => {
                                setStartDate(start);
                                setEndDate(end);
                            }} />
                        </Col>
                    </Row>
                    <Row className="mb-4">
                        <Col>
                            <PriceChart
                                data={getPrices}
                                chartType="line"
                                dataKey="prices"
                                xKey="dates"
                                title="Price Trend Over Time"
                            />
                        </Col>
                    </Row>
                    <Row className="mb-4">
                        <Col>
                            <PriceChart
                                data={averageYearlyData}
                                chartType="bar"
                                dataKey="Average_Price"
                                xKey="Year"
                                title="Average Yearly Price"
                            />
                        </Col>
                    </Row>
                    <Row className="mb-4">
                        <Col>
                            <PriceChart
                                data={priceDistributionData}
                                chartType="bar"
                                dataKey="Frequency"
                                xKey="PriceRange"
                                title="Price Distribution"
                            />
                        </Col>
                    </Row>
                    <Row className="mb-4">
                        <Col className="text-end">
                            <DataExport data={getPrices} />
                        </Col>
                    </Row>
                </Tab>

                {/* Event Impact Tab */}
                <Tab eventKey="event-impact" title="Event Impact">
                    <EventImpact /> {/* Display the EventImpact component in this tab */}
                </Tab>
            </Tabs>
        </Container>
    );
};

export default Dashboard;