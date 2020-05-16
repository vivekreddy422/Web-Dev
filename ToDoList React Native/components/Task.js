import React, { Component } from 'react';
import { Text, CheckBox, View, Button } from 'react-native';
import DatePicker from 'react-native-datepicker'

export default class Task extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        console.log(this.props.task.marked)
        if(this.props.task.marked) {
            return (
                <View style={{flexDirection: "row", flexWrap: "wrap", paddingBottom: 15, paddingTop: 15}}>
                    
                    <CheckBox onChange={() => {this.props.markTask(this.props.task.taskName)}}  value={this.props.task.marked}/>
                    <Text style={{textDecorationLine: 'line-through', 
                    textDecorationStyle: 'solid'}}>{this.props.task.taskName}</Text>
                    {/* <Text>{this.props.task.dueDate}</Text> */}
                    <Button title="Delete" onPress={() => {this.props.deleteTask(this.props.task.taskName) }}/>
                    <Text>{this.props.task.dueDate}</Text>
                </View>
            );
        }
        return (
            <View style={{flexDirection: "row", flexWrap: "wrap", paddingBottom: 15, paddingTop: 15}}>
                <CheckBox  onChange={() => {this.props.markTask(this.props.task.taskName)}} value={this.props.task.marked}/>
                <Text>{this.props.task.taskName}</Text>
                {/* <Text>{this.props.task.dueDate}</Text> */}
                <Button title="Delete" onPress={() => {this.props.deleteTask(this.props.task.taskName) }}/>
                <Text>{this.props.task.dueDate}</Text>
            </View>
        );
    }
}