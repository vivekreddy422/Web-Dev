import React, { Component } from 'react';
import { Text, CheckBox, View, Button } from 'react-native';

export default class Task extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        if(this.props.task.marked) {
            return (
                <View style={{flexDirection: "row", flexWrap: "wrap", paddingBottom: 15, paddingTop: 15}}>
                    <CheckBox onChange={() => {this.props.markTask(this.props.task.taskName)}}></CheckBox>
                    <Text style={{textDecorationLine: 'line-through', 
                    textDecorationStyle: 'solid'}}>{this.props.task.taskName}</Text>
                    <Text>{this.props.task.dueDate}</Text>
                    <Button title="Delete" onPress={() => {this.props.deleteTask(this.props.task.taskName) }}/>
                </View>
            );
        }
        return (
            <View style={{flexDirection: "row", flexWrap: "wrap", paddingBottom: 15, paddingTop: 15}}>
                <CheckBox checked={!this.props.task.marked} onChange={() => {this.props.markTask(this.props.task.taskName)}}></CheckBox>
                <Text>{this.props.task.taskName}</Text>
                <Text>{this.props.task.dueDate}</Text>
                <Button title="Delete" onPress={() => {this.props.deleteTask(this.props.task.taskName) }}/>
            </View>
        );
    }
}