import React, {Fragment, useRef} from 'react';
import {uid} from "react-uid";
import {withRouter} from 'react-router-dom';
import "../styles/DiceBoard.css"
import "../styles/CharacterStatsCard.css"

class CharacterStatsCard extends React.Component {

    state = {
        characterid: this.props.characterid,
        name: 'Olivia',
        status_effects: {HP: -1, STR: 0, DEX: 2, con: -1, int: 2, wis: -5, cha: 0},
        max_stats: {hp: 20, str: 12, dex: 13, con: 14, int: 15, wis: 16, cha: 17},
        current_stats: {}, // never directly set, always calculate this
        exp: 600,
        gold: 20,
        level: 3,
        toggleStatBreakdown: false,
        stat_breakdown: {"WIS":[
                                {name: "curse", amount: -1, description: "You really pissed the wizard off", duration: 12, duration_remaining: 10},
                                {name: "food poisoning", amount: -3, description: "Should you have drank that milk?", duration: 3, duration_remaining: 3}
                            ],
                        "STR": [
                                {name: "curse", amount: -1, description: "You really pissed the wizard off", duration: 12, duration_remaining: 10}]
    },
        selectedStat: "WIS"
    }
    // componentDidMount(){
    //     this.setCurrentStats()
    //     // this.props.socket.on("send_stat_breakdown", data => this.renderStatBreakdown(data))
    // }
    // state = {
    //     characterid: this.props.characterid,
    //     name: '',
    //     status_effects: {},
    //     max_stats: {},
    //     current_stats: {}, // never directly set, always calculate this
    //     exp: 0,
    //     gold: 0
    // }

    componentDidMount() {
        this.props.socket.emit("character_connected", {characterid: this.state.characterid})
        this.props.socket.on("character_setup", data => this.load_card(data))

        this.props.socket.on("get_character_changes", data=> this.reload_card(data))
        
    }
    load_card(data){
        console.log("loading")
        this.setState(data, () => this.setCurrentStats())
        console.log("status", this.state.status_effects)
        console.log("curr", this.state.current_stats)
        this.props.socket.off("character_setup")
    }
    reload_card(data){
        this.setState(data)
    }
    componentDidUpdate(prevProps, prevState){
        if (prevState.status_effects != this.state.status_effects || prevState.max_stats != this.state.max_stats){
            this.setCurrentStats()
        }

    }

    handleClickStat(stat){
        // this.props.socket.emit("get_stat_breakdown", {characterid: this.state.characterid, stat: stat})
        this.setState({toggleStatBreakdown: true, selectedStat: stat})
    }

    openStatBreakdown(stat){
        console.log("clicked")
        this.setState({selectedStat: stat})
        console.log(this.state.selectedStat)
        this.setState({toggleStatBreakdown: true})
    }
    closeStatBreakdown(){
        this.setState({toggleStatBreakdown: false})
    }
    setCurrentStats(){
        var newCurrStats = {}
        for (const key in this.state.max_stats){
            newCurrStats[key] = this.state.max_stats[key] + this.state.status_effects[key]
        }
        this.setState({current_stats: newCurrStats})
    }


    render(){
        const renderStatBreakdown = () => {
            if(this.state.toggleStatBreakdown){
                var effectJsonList = this.state.stat_breakdown[this.state.selectedStat] // [{name: name, amount: amount, description: description, duration: duration, duration_remaining: duration}]
                return(
                    <div className='statBreakdown'>
                        <button className='closeStatBreakdownButton' onClick={()=>this.closeStatBreakdown()}> x</button>
                        <ul className='status_effect_list'>
                            {effectJsonList.map((effect) =>(
                                <li className='status_effect'>
                                    <div>{effect["AMOUNT"]} {effect["NAME"]} ({effect["DURATION_REMAINING"]}/{effect["DURATION"]} turns left)</div>
                                    <div><i>{effect["DESCRIPTION"]}</i></div>
                                </li>
                            ))} 
                        </ul>
                    </div>
                )
            }
        }
        return(
            <div className='characterCardBody'>
                <button className='addStatusEffectButton'>+</button>
                <div className='characterName'><span className='nameHeader'>{this.state.name}</span></div>
                <div className='characterid'> <i>{this.state.characterid}</i></div>
                <div className='hpMpRow row'>
                    <div> HP: {this.state.current_stats["HP"]}/{this.state.max_stats["HP"]} </div>
                    
                </div>
                <div className='cumulativeStatsRow row'>
                    <div className='row'>
                        <div className='cumulativeStat'>Level {this.state.level} </div>
                        <div className='cumulativeStat'>Exp: {this.state.exp} </div>
                        <div className='cumulativeStat'>{this.state.gold} Gold </div>
                    </div>
                </div>
                <div className='inventory'>
                    <ul className='inventoryList'>

                    </ul>
                </div>
                <div className='statrow row'>
                    <div className='row'>
                        {["STR", "DEX", "CON", "INT", "WIS", "CHA"].map((stat)=>(
                            <div className='eachStat' onClick={ ()=> {this.openStatBreakdown(stat)}}>
                                <div>
                                    <b>{stat}</b>
                                </div>
                                <div>
                                <b>{this.state.current_stats[stat]}</b>
                                </div>
                                <div className='statDetails'>
                                
                                {
                                    this.state.status_effects[stat] >= 0 ? `(${this.state.max_stats[stat]}+${this.state.status_effects[stat]})` : 
                                    `(${this.state.max_stats[stat]}${this.state.status_effects[stat]})`
                                }

                                </div>
                                
                            </div>
                        
                        ))}
                    </div>
                </div>
                {renderStatBreakdown()}
            </div>
        )
    }

}

export default withRouter(CharacterStatsCard);