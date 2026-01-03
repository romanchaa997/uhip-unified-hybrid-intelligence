"""
Unit tests for Turbine RUL Prediction Model
Testing hybrid symbolic-neural inference logic
"""

import pytest
from datetime import datetime
from turbine_rul_model import TurbineRULModel, SensorData, PredictionResult


class TestTurbineRULModel:
    """Test suite for RUL prediction model."""

    @pytest.fixture
    def model(self):
        """Initialize model for tests."""
        return TurbineRULModel()

    @pytest.fixture
    def healthy_sensor_data(self):
        """Create sensor data representing healthy turbine."""
        return SensorData(
            vibration_rms=2.5,  # Well below critical (15.0)
            bearing_temp=45.0,  # Well below critical (90.0)
            generator_power=2.8,  # Good output
            gearbox_temp=55.0,  # Normal
            blade_pitch_angle=25.0,
            nacelle_wind_speed=10.5,
            generator_rpm=1200,
            timestamp=datetime.utcnow()
        )

    @pytest.fixture
    def degraded_sensor_data(self):
        """Create sensor data representing degraded turbine."""
        return SensorData(
            vibration_rms=10.5,  # Approaching critical
            bearing_temp=78.0,  # Close to critical
            generator_power=1.5,  # Reduced output
            gearbox_temp=82.0,  # Elevated
            blade_pitch_angle=35.0,
            nacelle_wind_speed=8.2,
            generator_rpm=950,
            timestamp=datetime.utcnow()
        )

    @pytest.fixture
    def critical_sensor_data(self):
        """Create sensor data representing critical condition."""
        return SensorData(
            vibration_rms=16.5,  # Above critical
            bearing_temp=92.0,  # Above critical
            generator_power=0.5,  # Severely reduced
            gearbox_temp=88.0,  # Above critical
            blade_pitch_angle=45.0,
            nacelle_wind_speed=3.2,
            generator_rpm=450,
            timestamp=datetime.utcnow()
        )

    def test_healthy_turbine_prediction(self, model, healthy_sensor_data):
        """Test prediction for healthy turbine."""
        result = model.predict(healthy_sensor_data)
        
        assert isinstance(result, PredictionResult)
        assert 0.8 < result.health_score <= 1.0, "Healthy turbine should have high health score"
        assert result.failure_risk_30d < 0.1, "Healthy turbine should have low failure risk"
        assert result.predicted_rul_hours > 8000, "Healthy turbine should have long RUL"
        assert len(result.warning_flags) == 0, "Healthy turbine should have no warnings"

    def test_degraded_turbine_prediction(self, model, degraded_sensor_data):
        """Test prediction for degraded turbine."""
        result = model.predict(degraded_sensor_data)
        
        assert 0.4 < result.health_score < 0.8, "Degraded turbine should have moderate health"
        assert 0.05 < result.failure_risk_30d < 0.3, "Degraded turbine should have moderate risk"
        assert 1000 < result.predicted_rul_hours < 8000, "RUL should be in normal range"
        assert len(result.top_risk_components) > 0, "Should identify risk components"

    def test_critical_turbine_prediction(self, model, critical_sensor_data):
        """Test prediction for critical turbine condition."""
        result = model.predict(critical_sensor_data)
        
        assert result.health_score < 0.4, "Critical turbine should have low health score"
        assert result.failure_risk_30d > 0.3, "Critical turbine should have high risk"
        assert result.predicted_rul_hours < 1000, "Critical turbine should have short RUL"
        assert len(result.warning_flags) > 0, "Critical condition should generate warnings"

    def test_health_score_calculation(self, model, healthy_sensor_data, degraded_sensor_data):
        """Test health score calculation."""
        healthy_score = model._calculate_health_score(healthy_sensor_data)
        degraded_score = model._calculate_health_score(degraded_sensor_data)
        
        assert healthy_score > degraded_score, "Healthy turbine should score higher"
        assert 0.0 <= healthy_score <= 1.0, "Health score must be in valid range"
        assert 0.0 <= degraded_score <= 1.0, "Health score must be in valid range"

    def test_failure_risk_calculation(self, model, healthy_sensor_data):
        """Test failure risk calculations."""
        risk_30d, risk_180d = model._calculate_failure_risks(healthy_sensor_data, None)
        
        assert 0.0 <= risk_30d <= 1.0, "30-day risk must be probability"
        assert 0.0 <= risk_180d <= 1.0, "180-day risk must be probability"
        assert risk_180d >= risk_30d, "180-day risk should be >= 30-day risk"

    def test_rul_estimation(self, model, healthy_sensor_data, degraded_sensor_data, critical_sensor_data):
        """Test RUL estimation across different health states."""
        healthy_score = model._calculate_health_score(healthy_sensor_data)
        degraded_score = model._calculate_health_score(degraded_sensor_data)
        critical_score = model._calculate_health_score(critical_sensor_data)
        
        healthy_rul = model._estimate_rul(healthy_sensor_data, healthy_score)
        degraded_rul = model._estimate_rul(degraded_sensor_data, degraded_score)
        critical_rul = model._estimate_rul(critical_sensor_data, critical_score)
        
        assert healthy_rul > degraded_rul > critical_rul, "RUL should decrease with health degradation"
        assert healthy_rul >= 168, "RUL should respect minimum (1 week)"
        assert critical_rul >= 168, "RUL should respect minimum (1 week)"

    def test_risk_component_identification(self, model, degraded_sensor_data):
        """Test identification of risk components."""
        risks = model._identify_risk_components(degraded_sensor_data)
        
        assert isinstance(risks, list), "Should return list"
        assert all("component" in r and "risk_type" in r and "probability" in r for r in risks), "Each risk should have required fields"
        assert all(0.0 <= r["probability"] <= 1.0 for r in risks), "Probabilities must be valid"
        assert len(risks) <= 3, "Should return max 3 risk components"

    def test_critical_condition_detection(self, model, critical_sensor_data, healthy_sensor_data):
        """Test critical alarm detection."""
        critical_warnings = model._check_critical_conditions(critical_sensor_data)
        healthy_warnings = model._check_critical_conditions(healthy_sensor_data)
        
        assert len(critical_warnings) > 0, "Should detect critical conditions"
        assert len(healthy_warnings) == 0, "Healthy turbine should have no warnings"
        assert any("CRITICAL" in w or "WARNING" in w for w in critical_warnings), "Warnings should be properly labeled"

    def test_confidence_estimation(self, model, healthy_sensor_data):
        """Test confidence interval estimation."""
        confidence = model._estimate_confidence(healthy_sensor_data, None)
        
        assert 0.5 <= confidence <= 1.0, "Confidence must be in valid range"
        
        # With historical data, confidence should increase
        historical_data = [healthy_sensor_data] * 10
        confidence_with_history = model._estimate_confidence(healthy_sensor_data, historical_data)
        
        assert confidence_with_history >= confidence, "Confidence should increase with historical data"

    def test_model_version(self, model):
        """Test model version tracking."""
        assert hasattr(model, 'model_version'), "Model should have version"
        assert model.model_version == "0.4.1", "Model version should match"

    def test_prediction_result_structure(self, model, healthy_sensor_data):
        """Test that prediction result has all required fields."""
        result = model.predict(healthy_sensor_data)
        
        required_fields = [
            'health_score', 'failure_risk_30d', 'failure_risk_180d',
            'predicted_rul_hours', 'top_risk_components', 'model_version',
            'inference_ts', 'confidence_interval', 'warning_flags'
        ]
        
        for field in required_fields:
            assert hasattr(result, field), f"Result should have {field}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
