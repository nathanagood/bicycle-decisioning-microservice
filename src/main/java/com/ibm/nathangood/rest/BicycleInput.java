package com.ibm.nathangood.rest;

/**
 * 
 */
public class BicycleInput {
    private Integer gearing;
    private String geometry;
    private Integer tireSize;

    public Integer getGearing() {
        return gearing;
    }

    public void setGearing(Integer gearing) {
        this.gearing = gearing;
    }

    public String getGeometry() {
        return geometry;
    }

    public void setGeometry(String geometry) {
        this.geometry = geometry;
    }

    public Integer getTireSize() {
        return tireSize;
    }

    public void setTireSize(Integer tireSize) {
        this.tireSize = tireSize;
    }
}
