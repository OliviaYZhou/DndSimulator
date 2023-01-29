import React, {Fragment, useRef} from 'react';
import {uid} from "react-uid";
import {withRouter} from 'react-router-dom';
import "../../styles/CharacterStatsCard.css"

class CharacterStatsCard extends React.Component {

    state = {
        characterid: this.props.characterid,
        character_type: '',
        name: 'No Name',
        status_effects: {HP: 0, STR: 0, DEX: 0, CON: 0, INT: 0, WIS: 0, CHA: 0},
        max_stats: {HP: 0, STR: 0, DEX: 0, CON: 0, INT: 0, WIS: 0, CHA: 0},
        current_stats: {}, // never directly set, always calculate this
        exp: 0,
        gold: 0,
        level: 0,
        toggleStatBreakdown: false,
        stat_breakdown: {"STR": [],"DEX": [],"CON": [],"INT": [],"WIS":[],"CHA": []},
        selectedStat: "",
        inventory: [], // item name: amount {"itemName": "bandage", "amount": 1}
        minimized: true
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
        // console.log("mount")
        // this.props.socket.emit("character_connected", {characterid: this.state.characterid}, function(error, message){
        //     console.log(error);
        //     console.log(message);
        // })
        // this.props.socket.on(`character_setup/${this.state.characterid}`, data => this.load_card(data))
        this.load_card()
        this.props.socket.on(`get_character_changes/${this.state.characterid}`, data=> this.reload_card(data))
        
    }
    load_card(data = {}){
        // characterid=${this.state.characterid

        fetch(`/api/character_connected/?characterid=${this.state.characterid}`, {
            headers : { 
              'Content-Type': 'application/json',
              'Accept': 'application/json'
             }
            }).then(res =>res.json())
            .then((data) => {
                console.log("api server call", data)
                this.setState(data, () => this.setCurrentStats())
            })

        // console.log("curr", this.state.current_stats)


        // console.log("loading")
        // console.log("loadcard", data)
        // this.setState(data, () => this.setCurrentStats())
        // console.log("status", this.state.status_effects)
        
        // this.props.socket.off(`character_setup/${this.state.characterid}`)
    }
    reload_card(data){
        this.setState(data, ()=> this.setCurrentStats())
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
        // console.log("clicked")
        this.setState({selectedStat: stat})
        // console.log(this.state.selectedStat)
        this.setState({toggleStatBreakdown: true})
    }
    closeStatBreakdown(){
        this.setState({toggleStatBreakdown: false})
    }
    toggleMinimizeCard(){
        this.setState({minimized: !this.state.minimized})
    }

    setCurrentStats(){
        // console.log("setCurrentStats", this.state.max_stats)
        var newCurrStats = {}
        for (const key in this.state.max_stats){
            newCurrStats[key] = this.state.max_stats[key] + this.state.status_effects[key]
        }
        newCurrStats["HP"] += newCurrStats["CON"]
        this.setState({current_stats: newCurrStats})
    }
    addStatusEffect(){
        this.props.showStatusForm()
    }


    render(){
        const renderStatBreakdown = () => {
            if(this.state.toggleStatBreakdown && !this.state.minimized){
                var effectJsonList = this.state.stat_breakdown[this.state.selectedStat] // [{name: name, amount: amount, description: description, duration: duration, duration_remaining: duration}]
                return(
                    <div className='statBreakdown'>
                        <button className='closeButton' onClick={()=>this.closeStatBreakdown()}> x</button>
                        <ul className='status_effect_list'>
                            {effectJsonList.map((effect) =>(
                                <li className='status_effect'>
                                    <div>{effect["AMOUNT"] >= 0 ? "+" : null}{effect["AMOUNT"]} {effect["NAME"]} ({effect["DURATION_REMAINING"]}/{effect["DURATION"]} turns left)</div>
                                    <div><i>{effect["DESCRIPTION"]}</i></div>
                                </li>
                            ))} 
                        </ul>
                    </div>
                )
            }
        }
        return(
            <div className='characterCardBody' style={{height: this.state.minimized ? "fit-content" : "400px"}}>
                <button className='addStatusEffectButton' onClick={()=>this.addStatusEffect()}>+</button>
                <div className='characterName' onClick={()=>{this.toggleMinimizeCard()}}><span className='nameHeader'>{this.state.name}</span></div>
                {this.state.minimized ? null : <div className='characterid'> <i>{this.state.characterid}</i></div>}
                
                <div className='hpMpRow row'>
                    <div> HP: {this.state.current_stats["HP"]}/{this.state.max_stats["HP"]+this.state.current_stats["CON"]} </div>
                    
                </div>
                
                <div className='cumulativeStatsRow row'>
                    <div className='row'>
                        <div className='cumulativeStat'>Level {this.state.level} </div>
                        <div className='cumulativeStat'>Exp: {this.state.exp} </div>
                        <div className='cumulativeStat'>{this.state.gold} Gold </div>
                        {/* {this.state.character_type == "PLAYER" ? 
                        <Fragment>
                            <div className='cumulativeStat'>Exp: {this.state.exp} </div>
                            <div className='cumulativeStat'>{this.state.gold} Gold </div>
                        </Fragment> 
                        : null} */}
                        
                    </div>
                </div>
                <div className='inventoryWrapper' style={{height: this.state.minimized ? "0px" : "120px"}}>
                    <ul className='inventoryList'>
                        {this.state.inventory.map((itemJson) => (
                            <li>
                                {itemJson["amount"]} x {itemJson["itemName"]}
                            </li>
                        ))}
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
                                
                                { this.state.minimized ? null :
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