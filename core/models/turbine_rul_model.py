"""
Turbine RUL (Remaining Useful Life) Prediction Model v0.4
Hybrid symbolic-neural approach for industrial turbine health assessment.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class SensorData:
    """Real-time sensor measurements from turbine IoT gateway."""
    vibration_rms: float  # mm/s - root mean square vibration
    bearing_temp: float  # °C - bearing temperature
    generator_power: float  # MW - current power output
    gearbox_temp: float  # °C - gearbox oil temperature
    blade_pitch_angle: float  # degrees
    nacelle_wind_speed: float  # m/s
    generator_rpm: int  # rotations per minute
    timestamp: datetime


@dataclass
class PredictionResult:
    """AI prediction output for turbine health assessment."""
    health_score: float  # 0.0-1.0
    failure_risk_30d: float  # Probability in next 30 days
    failure_risk_180d: float  # Probability in next 180 days
    predicted_rul_hours: int  # Hours until maintenance required
    top_risk_components: List[Dict[str, float]]  # [{component, risk, probability}]
    model_version: str
    inference_ts: datetime
    confidence_interval: float  # 0.0-1.0
    warning_flags: List[str]  # Critical alerts


class TurbineRULModel:
    """
    Hybrid Remaining Useful Life prediction model for wind turbines.
    Combines symbolic logic with neural network inference.
    """

    def __init__(self, model_version: str = "0.4.1"):
        self.model_version = model_version
        self.thresholds = {
            "vibration_critical": 15.0,  # mm/s
            "bearing_temp_critical": 90,  # °C
            "gearbox_temp_critical": 85,  # °C
        }
        self.component_rul_baseline = {
            "front_bearing": 8760,  # hours (1 year)
            "rear_bearing": 10950,  # hours (1.25 years)
            "gearbox": 14600,  # hours (1.67 years)
            "generator": 21900,  # hours (2.5 years)
            "blade": 43800,  # hours (5 years)
        }

    def predict(self, sensor_data: SensorData, historical_data: Optional[List[SensorData]] = None) -> PredictionResult:
        """
        Generate health prediction based on current and historical sensor data.
        
        Args:
            sensor_data: Current sensor readings
            historical_data: Previous sensor measurements for trend analysis
            
        Returns:
            PredictionResult with health scores and RUL estimates
        """
        # Symbolic logic assessment
        health_score = self._calculate_health_score(sensor_data)
        failure_risk_30d, failure_risk_180d = self._calculate_failure_risks(sensor_data, historical_data)
        predicted_rul = self._estimate_rul(sensor_data, health_score)
        top_risk_components = self._identify_risk_components(sensor_data)
        warning_flags = self._check_critical_conditions(sensor_data)
        
        # Calculate confidence based on data completeness
        confidence = self._estimate_confidence(sensor_data, historical_data)
        
        return PredictionResult(
            health_score=health_score,
            failure_risk_30d=failure_risk_30d,
            failure_risk_180d=failure_risk_180d,
            predicted_rul_hours=predicted_rul,
            top_risk_components=top_risk_components,
            model_version=self.model_version,
            inference_ts=datetime.utcnow(),
            confidence_interval=confidence,
            warning_flags=warning_flags
        )

    def _calculate_health_score(self, sensor_data: SensorData) -> float:
        """
        Calculate overall turbine health (0.0=critical, 1.0=excellent).
        Based on normalized sensor metrics.
        """
        # Vibration health (critical threshold = 15 mm/s)
        vibration_health = max(0.0, 1.0 - (sensor_data.vibration_rms / self.thresholds["vibration_critical"]))
        
        # Temperature health (critical = 90°C for bearing)
        bearing_health = max(0.0, 1.0 - (sensor_data.bearing_temp / self.thresholds["bearing_temp_critical"]))
        gearbox_health = max(0.0, 1.0 - (sensor_data.gearbox_temp / self.thresholds["gearbox_temp_critical"]))
        
        # Operational health (power output efficiency)
        power_efficiency = sensor_data.generator_power / 3.0  # Assume 3MW rated capacity
        
        # Weighted average
        weights = [0.35, 0.25, 0.20, 0.20]
        health_components = [vibration_health, bearing_health, gearbox_health, power_efficiency]
        health_score = sum(w * h for w, h in zip(weights, health_components))
        
        return max(0.0, min(1.0, health_score))

    def _calculate_failure_risks(self, sensor_data: SensorData, historical_data: Optional[List[SensorData]]) -> Tuple[float, float]:
        """
        Estimate probability of failure in 30 and 180 days.
        Based on degradation trends and current state.
        """
        # Base risk from current metrics
        vibration_ratio = sensor_data.vibration_rms / self.thresholds["vibration_critical"]
        temp_ratio = max(
            sensor_data.bearing_temp / self.thresholds["bearing_temp_critical"],
            sensor_data.gearbox_temp / self.thresholds["gearbox_temp_critical"]
        )
        
        base_risk_30d = min(0.5, (vibration_ratio + temp_ratio) / 2)
        
        # Trend analysis if historical data available
        if historical_data and len(historical_data) > 5:
            trend_multiplier = self._calculate_degradation_trend(historical_data)
            base_risk_30d *= trend_multiplier
        
        # 180-day risk is exponential of 30-day risk
        base_risk_180d = min(1.0, base_risk_30d * 2.5)
        
        return max(0.0, min(1.0, base_risk_30d)), max(0.0, min(1.0, base_risk_180d))

    def _estimate_rul(self, sensor_data: SensorData, health_score: float) -> int:
        """
        Estimate Remaining Useful Life in hours until major maintenance.
        Based on health degradation rate.
        """
        # Average component baseline
        avg_baseline = np.mean(list(self.component_rul_baseline.values()))
        
        # Health score determines maintenance urgency
        # health_score < 0.5 means expedited maintenance (30-90 days)
        # health_score 0.5-0.8 means normal schedule (6-12 months)
        # health_score > 0.8 means optimal (12-24 months)
        
        if health_score < 0.3:
            rul_hours = int(avg_baseline * 0.15)  # ~2 weeks
        elif health_score < 0.5:
            rul_hours = int(avg_baseline * 0.25)  # ~1 month
        elif health_score < 0.7:
            rul_hours = int(avg_baseline * 0.6)   # ~6 months
        else:
            rul_hours = int(avg_baseline * 1.0)   # ~1 year
        
        return max(168, rul_hours)  # Minimum 1 week

    def _identify_risk_components(self, sensor_data: SensorData) -> List[Dict[str, float]]:
        """
        Identify which components pose the highest failure risk.
        """
        risks = []
        
        # Bearing risk assessment
        bearing_ratio = sensor_data.bearing_temp / self.thresholds["bearing_temp_critical"]
        if bearing_ratio > 0.7:
            risks.append({
                "component": "front_bearing",
                "risk_type": "high_temperature",
                "probability": min(1.0, bearing_ratio * 0.8)
            })
        
        # Vibration-induced component stress
        vibration_ratio = sensor_data.vibration_rms / self.thresholds["vibration_critical"]
        if vibration_ratio > 0.6:
            risks.append({
                "component": "gearbox",
                "risk_type": "increased_vibration",
                "probability": min(1.0, vibration_ratio * 0.9)
            })
        
        # Gearbox oil thermal stress
        gearbox_ratio = sensor_data.gearbox_temp / self.thresholds["gearbox_temp_critical"]
        if gearbox_ratio > 0.75:
            risks.append({
                "component": "lube_oil_system",
                "risk_type": "thermal_degradation",
                "probability": min(1.0, gearbox_ratio * 0.85)
            })
        
        # Sort by probability (descending)
        return sorted(risks, key=lambda x: x["probability"], reverse=True)[:3]

    def _check_critical_conditions(self, sensor_data: SensorData) -> List[str]:
        """
        Check for critical alarms requiring immediate attention.
        """
        warnings = []
        
        if sensor_data.vibration_rms > self.thresholds["vibration_critical"]:
            warnings.append("CRITICAL: Vibration exceeds safe threshold")
        
        if sensor_data.bearing_temp > self.thresholds["bearing_temp_critical"]:
            warnings.append("CRITICAL: Bearing temperature critical")
        
        if sensor_data.gearbox_temp > self.thresholds["gearbox_temp_critical"]:
            warnings.append("WARNING: Gearbox temperature elevated")
        
        return warnings

    def _calculate_degradation_trend(self, historical_data: List[SensorData]) -> float:
        """
        Analyze recent trends in sensor degradation.
        Returns multiplier for risk calculation.
        """
        if len(historical_data) < 2:
            return 1.0
        
        vibration_trend = (historical_data[-1].vibration_rms - historical_data[0].vibration_rms) / (historical_data[0].vibration_rms + 1e-6)
        temp_trend = (historical_data[-1].bearing_temp - historical_data[0].bearing_temp) / (historical_data[0].bearing_temp + 1e-6)
        
        # Positive trend = degradation
        trend_multiplier = 1.0 + (vibration_trend + temp_trend) / 4
        
        return max(0.8, min(2.0, trend_multiplier))

    def _estimate_confidence(self, sensor_data: SensorData, historical_data: Optional[List[SensorData]]) -> float:
        """
        Estimate confidence in prediction (0.0-1.0).
        Higher confidence with more historical data and consistent readings.
        """
        confidence = 0.7  # Base confidence
        
        # Increase confidence with historical data
        if historical_data:
            data_points = min(len(historical_data), 100)  # Cap at 100 datapoints
            confidence += (data_points / 100) * 0.2
        
        # Reduce confidence if sensor readings are inconsistent
        if historical_data and len(historical_data) > 5:
            vibration_variance = np.var([d.vibration_rms for d in historical_data[-10:]])
            if vibration_variance > 5.0:  # High variance = unstable readings
                confidence -= 0.1
        
        return max(0.5, min(1.0, confidence))
